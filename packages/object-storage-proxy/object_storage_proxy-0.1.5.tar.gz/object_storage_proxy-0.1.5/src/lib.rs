#![warn(clippy::all)]

use tracing::{error, info};

use tracing_subscriber::EnvFilter;
use tracing_subscriber::fmt::time::ChronoLocal;

use pyo3::prelude::*;

use async_trait::async_trait;
use http::Uri;
use http::uri::Authority;

use pyo3::types::{PyModule, PyModuleMethods};
use pyo3::{Bound, PyResult, Python, pyclass, pyfunction, pymodule, wrap_pyfunction};
use std::collections::HashMap;
use std::fmt::Debug;

use std::sync::Mutex;

use dotenv::dotenv;
use pingora::Result;
use pingora::proxy::{ProxyHttp, Session};
use pingora::server::Server;
use pingora::upstreams::peer::HttpPeer;

pub mod parsers;
use parsers::path::parse_path;

pub mod credentials;

pub mod utils;
use credentials::secrets_proxy::{SecretsCache, get_bearer};


static REQ_COUNTER: Mutex<usize> = Mutex::new(0);

#[pyclass]
#[pyo3(name = "ProxyServerConfig")]
#[derive(Debug)]
pub struct ProxyServerConfig {
    #[pyo3(get, set)]
    pub bucket_creds_fetcher: Option<Py<PyAny>>,

    #[pyo3(get, set)]
    pub cos_map: PyObject,

    #[pyo3(get, set)]
    pub port: u16,

    #[pyo3(get, set)]
    pub validator: Option<Py<PyAny>>,
}

impl Default for ProxyServerConfig {
    fn default() -> Self {
        ProxyServerConfig {
            bucket_creds_fetcher: None,
            cos_map: Python::with_gil(|py| py.None()),
            port: 6190,
            validator: None,
        }
    }
}

#[pymethods]
impl ProxyServerConfig {
    #[new]
    pub fn new(
        bucket_creds_fetcher: Option<PyObject>,
        cos_map: PyObject,
        port: u16,
        validator: Option<PyObject>,
    ) -> Self {
        ProxyServerConfig {
            bucket_creds_fetcher: bucket_creds_fetcher.map(|obj| obj.into()),
            cos_map,
            port,
            validator: validator.map(|obj| obj.into()),
        }
    }
}

#[derive(FromPyObject, Debug, Clone)]
pub struct CosMapItem {
    pub host: String,
    pub port: u16,
    pub api_key: Option<String>,
}

fn parse_cos_map(py: Python, cos_dict: &PyObject) -> PyResult<HashMap<String, CosMapItem>> {
    let mut cos_map: HashMap<String, CosMapItem> = HashMap::new();
    // let cos_tuples: Result<Vec<(String, String, u16, Option<String>)>, PyErr> =
    //     cos_dict.extract(py);
    
    let tuples: Vec<(String, String, u16, Option<String>)> = cos_dict.extract(py)?;
    for (bucket, host, port, api_key) in tuples {
        let host = host.to_string();
        let port = port;
        let bucket = bucket.to_string();
        let api_key = api_key.map(|s| s.to_string());

        cos_map.insert(
            bucket.clone(),
            CosMapItem {
                host: host.clone(),
                port,
                api_key: api_key.clone(),
            },
        );
    };

    Ok(cos_map)


}

pub struct MyProxy {
    cos_endpoint: String,
    cos_mapping: HashMap<String, CosMapItem>,
    secrets_cache: SecretsCache,
    validator: Option<PyObject>,
}

pub struct MyCtx {
    cos_mapping: HashMap<String, CosMapItem>,
    secrets_cache: SecretsCache,
    validator: Option<PyObject>,
}

#[async_trait]
impl ProxyHttp for MyProxy {
    type CTX = MyCtx;
    fn new_ctx(&self) -> Self::CTX {
        MyCtx {
            cos_mapping: self.cos_mapping.clone(),
            secrets_cache: self.secrets_cache.clone(),
            validator: self
                .validator
                .as_ref()
                .map(|v| Python::with_gil(|py| v.clone_ref(py))),
        }
    }

    // TODO: cache authorization like we do for bearer tokens
    async fn request_filter(
        &self,
        session: &mut Session,
        ctx: &mut Self::CTX,
    ) -> Result<bool> {

        
        let path = session.req_header().uri.path();

        let parse_path_result = parse_path(path);
        if parse_path_result.is_err() {
            error!("Failed to parse path: {:?}", parse_path_result);
            return Err(pingora::Error::new_str("Failed to parse path"));
        }

        let (_, (bucket, _)) = parse_path(path).unwrap();

        let auth_header = session
            .req_header()
            .headers
            .get("authorization")
            .map(|h| h.to_str().unwrap())
            .unwrap_or("");

        let is_authorized = if let Some(py_cb) = &ctx.validator {
            Python::with_gil(|py| {
                crate::utils::validator::validate_request(
                    auth_header,
                    &bucket,
                    py,
                    py_cb,
                )
                .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e))
                .and_then(|ok| Ok(ok))
            })
            .map_err(|_| pingora::Error::new_str("Python validator panicked"))?
        } else {
            true
        };

        if !is_authorized {
            session.respond_error(401).await?;
            return Ok(true);
        }

        Ok(false)
    }


    async fn upstream_peer(
        &self,
        session: &mut Session,
        ctx: &mut Self::CTX,
    ) -> Result<Box<HttpPeer>> {
        let mut req_counter = REQ_COUNTER.lock().unwrap();
        *req_counter += 1;


        let path = session.req_header().uri.path();

        let parse_path_result = parse_path(path);
        if parse_path_result.is_err() {
            error!("Failed to parse path: {:?}", parse_path_result);
            return Err(pingora::Error::new_str("Failed to parse path"));
        }

        let (_, (bucket, _)) = parse_path(path).unwrap();

        let hdr_bucket = bucket.to_owned();


        let bucket_config = ctx.cos_mapping.get(&hdr_bucket);
        let endpoint = match bucket_config {
            Some(config) => {
                format!("{}", config.host)
            }
            None => {
                format!("{}.{}", bucket, self.cos_endpoint)
            }
        };

        let addr = (endpoint.clone(), 443);


        let mut peer = Box::new(HttpPeer::new(addr, true, endpoint.clone()));
        peer.options.verify_cert = false;
        Ok(peer)
    }

    async fn upstream_request_filter(
        &self,
        _session: &mut Session,
        upstream_request: &mut pingora::http::RequestHeader,
        ctx: &mut Self::CTX,
    ) -> Result<()> {

        let (_, (bucket, my_updated_url)) = parse_path(upstream_request.uri.path()).unwrap();

        let hdr_bucket = bucket.to_string();

        let my_query = match upstream_request.uri.query() {
            Some(q) if !q.is_empty() => format!("?{}", q),
            _ => String::new(),
        };

        let bucket_config = ctx.cos_mapping.get(&hdr_bucket);

        let endpoint = match bucket_config {
            Some(config) => {
                format!("{}.{}", bucket, config.host)
            }
            None => {
                format!("{}.{}", bucket, self.cos_endpoint)
            }
        };
        let api_key = match bucket_config {
            Some(config) => config.api_key.clone(),
            None => None,
        };

        let Some(api_key) = api_key else {
            error!("No API key configured for bucket: {}", hdr_bucket);
            return Err(pingora::Error::new_str("No API key configured for bucket"));
        };

        let bearer_fetcher = {
            let api_key = api_key.clone();
            move || get_bearer(api_key.clone())
        };

        let bearer_token = ctx.secrets_cache.get(&hdr_bucket, bearer_fetcher).await;

        // Box:leak the temporary string to get a static reference which will outlive the function
        let authority = Authority::from_static(Box::leak(endpoint.clone().into_boxed_str()));

        let new_uri = Uri::builder()
            .scheme("https")
            .authority(authority.clone())
            .path_and_query(my_updated_url.to_owned() + &my_query)
            .build()
            .expect("should build a valid URI");

        info!("Sending request to upstream: {}", &new_uri);

        upstream_request.set_uri(new_uri);

        upstream_request.insert_header("host", authority.as_str())?;

        upstream_request
            .insert_header("Authorization", format!("Bearer {}", bearer_token.unwrap()))?;

        info!("Request sent to upstream.");


        Ok(())
    }
}

pub fn init_tracing() {
    tracing_subscriber::fmt()
        .with_timer(ChronoLocal::rfc_3339())
        .with_env_filter(EnvFilter::from_default_env())
        .init();
}

pub fn run_server(py: Python, run_args: &ProxyServerConfig) {
    init_tracing();
    info!(
        "Logger initialized; starting server on port {}",
        run_args.port
    );

    match run_args.bucket_creds_fetcher {
        Some(ref fetcher) => {
            info!("Bucket creds fetcher provided: {:?}", fetcher);
            let _d = get_api_key_for_bucket(py, fetcher, "bucket01".to_string());
        }
        None => {
            info!("No bucket creds fetcher provided");
        }
    }
    dbg!(&run_args.cos_map);
    let cosmap = parse_cos_map(py, &run_args.cos_map).unwrap();

    let mut my_server = Server::new(None).unwrap();
    my_server.bootstrap();

    let validator = run_args.validator.as_ref().map(|v| v.clone_ref(py));

    let mut my_proxy = pingora::proxy::http_proxy_service(
        &my_server.configuration,
        MyProxy {
            cos_endpoint: "s3.eu-de.cloud-object-storage.appdomain.cloud".to_string(),
            cos_mapping: cosmap,
            secrets_cache: SecretsCache::new(),
            validator,
        },
    );
    my_proxy.add_tcp("0.0.0.0:6190");

    my_server.add_service(my_proxy);

    // my_server.run_forever()
    py.allow_threads(|| my_server.run_forever());

    info!("server running ...");
}

fn get_api_key_for_bucket(py: Python, callback: &PyObject, bucket: String) -> PyResult<()> {
    match callback.call1(py, (bucket,)) {
        Ok(result) => {
            let content = result.extract::<String>(py)?;
            info!("Callback returned: {}...", content.chars().take(4).collect::<String>());
            Ok(())
        }
        Err(err) => {
            error!("Python callback raised an exception: {:?}", err);
            return Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                "Failed to call callback due to an inner Python exception",
            ));
        }
    }
}

#[pyfunction]
pub fn start_server(py: Python, run_args: &ProxyServerConfig) -> PyResult<()> {
    rustls::crypto::ring::default_provider().install_default().expect("Failed to install rustls crypto provider");

    dotenv().ok();

    run_server(py, &run_args);

    Ok(())
}

#[pymodule]
fn object_storage_proxy(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(start_server, m)?)?;
    m.add_class::<ProxyServerConfig>()?;
    Ok(())
}

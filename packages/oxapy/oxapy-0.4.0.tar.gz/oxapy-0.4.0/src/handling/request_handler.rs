use std::{collections::HashMap, mem::transmute, sync::Arc};

use http_body_util::{BodyExt, Full};
use hyper::{
    body::{Bytes, Incoming},
    Request as HyperRequest, Response as HyperResponse,
};
use pyo3::{Py, PyAny};
use tokio::sync::mpsc::{channel, Sender};

use crate::{
    cors::Cors,
    into_response::IntoResponse,
    multipart::{parse_mutltipart, MultiPart},
    request::Request,
    response::Response,
    routing::Router,
    status::Status,
    templating::Template,
    IntoPyException, MatchitRoute, ProcessRequest,
};

pub async fn handle_request(
    req: HyperRequest<Incoming>,
    request_sender: Sender<ProcessRequest>,
    routers: Vec<Arc<Router>>,
    app_data: Option<Arc<Py<PyAny>>>,
    channel_capacity: usize,
    cors: Option<Arc<Cors>>,
    template: Option<Arc<Template>>,
) -> Result<HyperResponse<Full<Bytes>>, hyper::http::Error> {
    if req.method() == hyper::Method::OPTIONS && cors.is_some() {
        let response = cors.as_ref().unwrap().into_response().unwrap();
        return convert_to_hyper_response(response);
    }

    let request = convert_hyper_request(req, app_data, template)
        .await
        .unwrap();

    for router in &routers {
        if let Some(route) = router.find(&request.method, &request.uri) {
            let (response_sender, mut respond_receive) = channel(channel_capacity);

            let route: MatchitRoute = unsafe { transmute(&route) };

            let process_request = ProcessRequest {
                request: request.clone(),
                router: router.clone(),
                route,
                response_sender,
                cors: cors.clone(),
            };

            if request_sender.send(process_request).await.is_ok() {
                if let Some(response) = respond_receive.recv().await {
                    return convert_to_hyper_response(response);
                }
            }
            break;
        }
    }

    let response = if let Some(cors_config) = cors {
        cors_config.apply_to_response(Status::NOT_FOUND.into_response().unwrap())
    } else {
        Status::NOT_FOUND.into_response()
    };

    convert_to_hyper_response(response.unwrap())
}

async fn convert_hyper_request(
    req: HyperRequest<Incoming>,
    app_data: Option<Arc<Py<PyAny>>>,
    template: Option<Arc<Template>>,
) -> Result<Arc<Request>, Box<dyn std::error::Error + Sync + Send>> {
    let method = req.method().to_string();
    let uri = req.uri().to_string();

    let mut headers = HashMap::new();
    for (key, value) in req.headers() {
        headers.insert(
            key.to_string(),
            value.to_str().unwrap_or_default().to_string(),
        );
    }

    let mut request = Request::new(method, uri, headers.clone());

    let body_bytes = req.collect().await?.to_bytes();
    let body = String::from_utf8_lossy(&body_bytes).to_string();

    if let Some(content_type) = headers.get("content-type") {
        if content_type.starts_with("multipart/form-data") {
            let MultiPart { fields, files } = parse_mutltipart(content_type, body_bytes)
                .await
                .into_py_exception()?;
            request.form_data = Some(fields);
            request.files = Some(files);
        }
    }

    if !body.is_empty() {
        request.body = Some(body);
    }

    request.app_data = app_data;
    request.template = template;

    Ok(Arc::new(request))
}

fn convert_to_hyper_response(
    response: Response,
) -> Result<HyperResponse<Full<Bytes>>, hyper::http::Error> {
    let mut response_builder = HyperResponse::builder().status(response.status.code());
    for (key, value) in response.headers {
        response_builder = response_builder.header(key, value);
    }
    response_builder.body(Full::new(response.body))
}

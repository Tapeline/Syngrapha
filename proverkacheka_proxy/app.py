import logging
import os
from datetime import datetime

import uvicorn
from asgi_monitor.integrations.fastapi import (
    MetricsConfig,
    TracingConfig,
    setup_metrics, setup_tracing,
)
from asgi_monitor.logging import configure_logging
from asgi_monitor.tracing import span
from fastapi import APIRouter, FastAPI, Response
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from parser import ProverkaChekaComClient

TEMPO_ENDPOINT = os.environ.get(
    "TEMPO_ENDPOINT",
    "http://localhost:4317"
)

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
router = APIRouter(prefix="")
client = ProverkaChekaComClient(logger)


@router.get("/get-check")
@span
def get_check(t: str, s: str, fn: int, i: int, fp: int, response: Response):
    extra = {"t": t, "s": s, "fn": fn, "i": i, "fp": fp}
    logger.info("check requested", extra=extra)
    try:
        dt = datetime.strptime(t, "%Y%m%dT%H%M")
    except ValueError:
        response.status_code = 400
        return {"t": "invalid"}
    html = client.get_check_html(
        fn=fn, s=s, fp=fp, fd=i, d=dt.strftime("%d%m%Y"),
        t=dt.strftime("%H%M")
    )
    if not html:
        logger.info("check not found", extra=extra)
        response.status_code = 404
        return None
    with tracer.start_as_current_span("parsing"):
        return dt, *client.parse_html_contents(html)


app = FastAPI()
configure_logging(level=logging.INFO, json_format=True, include_trace=True)
resource = Resource.create(
    attributes={
        "service.name": "pc_proxy",
    },
)
tracer_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer_provider)
tracer_provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint=TEMPO_ENDPOINT))
)

trace_config = TracingConfig(tracer_provider=tracer_provider)
metrics_config = MetricsConfig(
    app_name="pc_proxy", include_trace_exemplar=True
)
app.include_router(router)

setup_metrics(app=app, config=metrics_config)
setup_tracing(app=app, config=trace_config)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888, log_config=None)

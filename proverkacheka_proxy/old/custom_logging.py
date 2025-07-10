import json
import time
from logging import Formatter, Logger

from starlette.middleware.base import BaseHTTPMiddleware


EXCLUDE = {
    "levelno", "pathname", "filename", "module", "relativeCreated",
    "msecs", "stack_info", "threadName", "processName", "process",
    "taskName", "lineno", "thread", "funcName"
}


class JsonFormatter(Formatter):
    def format(self, record):
        return json.dumps({
            k: v for k, v in record.__dict__.items() if k not in EXCLUDE
        })


class LogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, logger: Logger):
        self.logger = logger
        super().__init__(app)

    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            end = time.perf_counter()
            self.logger.error(
                "Internal server error",
                extra={
                    "req": {
                        "method": request.method, "url": str(request.url),
                    },
                    "res": {
                        "status_code": 500,
                    },
                    "time_ms": (end - start) * 1000,
                },
            )
            return None
        else:
            end = time.perf_counter()
            self.logger.info(
                "Incoming request",
                extra={
                    "req": {
                        "method": request.method, "url": str(request.url),
                    },
                    "res": {
                        "status_code": response.status_code,
                    },
                    "time_ms": (end - start) * 1000,
                },
            )
        return response

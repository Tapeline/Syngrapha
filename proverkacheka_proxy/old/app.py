import logging
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Response

from custom_logging import JsonFormatter, LogMiddleware
from parser import ProverkaChekaComClient

logger = logging.getLogger("app")
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.handlers = [handler]
logger.setLevel(logging.INFO)
app = FastAPI()
app.add_middleware(LogMiddleware, logger=logger)
client = ProverkaChekaComClient(logger)
logging.getLogger("uvicorn.access").handlers.clear()
logging.getLogger("uvicorn").handlers.clear()


@app.get("/get-check")
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
    return dt, *client.parse_html_contents(html)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888, log_config=None)

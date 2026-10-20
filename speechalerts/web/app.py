"""FastAPI app: live alert feed over server-sent events plus a JSON history endpoint."""

from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from sse_starlette.sse import EventSourceResponse

from speechalerts.config import settings
from speechalerts.sinks.broadcast import BroadcastSink
from speechalerts.sinks.sqlite import SqliteSink

log = logging.getLogger(__name__)
STATIC = Path(__file__).parent / "static"


def create_app(broadcast: BroadcastSink, db: SqliteSink | None = None) -> FastAPI:
    app = FastAPI(title="Speech Alerts")

    @app.get("/", response_class=HTMLResponse)
    async def index() -> str:
        return (STATIC / "index.html").read_text()

    @app.get("/api/status")
    async def status() -> JSONResponse:
        return JSONResponse(broadcast.status)

    @app.get("/api/alerts")
    async def alerts(limit: int = 100) -> JSONResponse:
        if db is not None:
            return JSONResponse(db.recent_alerts(limit))
        return JSONResponse(list(broadcast.recent_alerts)[:limit])

    @app.get("/api/transcript")
    async def transcript() -> JSONResponse:
        return JSONResponse(list(broadcast.recent_segments))

    @app.get("/events")
    async def events():
        queue = broadcast.subscribe()

        async def gen():
            try:
                yield {"event": "status", "data": json.dumps(broadcast.status)}
                for a in reversed(list(broadcast.recent_alerts)[:50]):
                    yield {"event": "alert", "data": json.dumps(a)}
                while True:
                    try:
                        payload = await asyncio.wait_for(queue.get(), timeout=15)
                    except asyncio.TimeoutError:
                        yield {"event": "ping", "data": "{}"}
                        continue
                    msg = json.loads(payload)
                    yield {"event": msg["event"], "data": json.dumps(msg["data"])}
            finally:
                broadcast.unsubscribe(queue)

        return EventSourceResponse(gen())

    return app


async def serve(app: FastAPI, host: str | None = None, port: int | None = None) -> None:
    config = uvicorn.Config(
        app, host=host or settings.web_host, port=port or settings.web_port, log_level="warning", loop="asyncio"
    )
    server = uvicorn.Server(config)
    log.info("web UI on http://%s:%d", config.host, config.port)
    await server.serve()

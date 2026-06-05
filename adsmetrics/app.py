from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from . import data as data_mod
from . import metrics as metrics_mod
from .dashboard import render

_state: dict = {}


@asynccontextmanager
async def lifespan(_app: FastAPI):
    _state["metrics"] = metrics_mod.compute(data_mod.generate())
    yield


app = FastAPI(title="Advertising & Profitability Metrics", lifespan=lifespan)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/api/metrics")
def api_metrics():
    return _state["metrics"]


@app.get("/", response_class=HTMLResponse)
def dashboard():
    return render(_state["metrics"])

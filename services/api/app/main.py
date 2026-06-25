"""Recurve Data API.

Three jobs, all tenant-scoped:
  POST /v1/connect          store an encrypted Stripe restricted key, kick off ingest
  POST /v1/run/{tenant_id}  trigger that tenant's pipeline
  GET  /v1/metrics/...      serve aggregated, tenant-scoped metrics from the warehouse

Only /health is implemented in the scaffold. The rest are wired in P3 once the
pipeline and auth are in place; they return 501 until then so nothing pretends
to work.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .config import get_settings

settings = get_settings()

app = FastAPI(
    title="Recurve Data API",
    version="0.1.0",
    summary="Tenant-scoped subscription-revenue metrics.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health", tags=["meta"])
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


class ConnectRequest(BaseModel):
    tenant_id: str = Field(..., description="Tenant the connection belongs to.")
    # A Stripe RESTRICTED key (rk_...). We reject unrestricted secret keys.
    restricted_key: str = Field(..., min_length=10)
    mode: str = Field("test", pattern="^(test|live)$")


@app.post("/v1/connect", tags=["connections"], status_code=status.HTTP_501_NOT_IMPLEMENTED)
def connect(_: ConnectRequest) -> None:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="connect is wired up in P3 (encrypt key -> store -> kick ingest).",
    )


@app.post("/v1/run/{tenant_id}", tags=["pipeline"], status_code=status.HTTP_501_NOT_IMPLEMENTED)
def run(tenant_id: str) -> None:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="pipeline trigger is wired up in P3 (Dagster run for this tenant).",
    )


@app.get("/v1/metrics/{tenant_id}/overview", tags=["metrics"], status_code=status.HTTP_501_NOT_IMPLEMENTED)
def metrics_overview(tenant_id: str) -> None:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="metrics are served in P3 once the marts exist.",
    )

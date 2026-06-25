# Data API (FastAPI)

Tenant-scoped metrics over the warehouse. Deploys to Cloud Run (scale-to-zero);
runs locally via docker-compose or directly with uvicorn.

## Run locally

From the repo root:

```bash
uv run uvicorn services.api.app.main:app --reload --port 8000
```

Then `GET http://localhost:8000/health` and the docs at `/docs`.

## Endpoints

| Method | Path                          | Status   | Notes                                     |
| ------ | ----------------------------- | -------- | ----------------------------------------- |
| GET    | `/health`                     | done     | liveness                                  |
| POST   | `/v1/connect`                 | P3       | store encrypted restricted key, ingest    |
| POST   | `/v1/run/{tenant_id}`         | P3       | trigger this tenant's pipeline            |
| GET    | `/v1/metrics/{tenant_id}/...` | P3       | tenant-scoped metrics from the marts      |

Auth (Clerk session check) and per-tenant authorization land in P3 — every route
must prove the caller belongs to the tenant before returning a single row.

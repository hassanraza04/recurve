# Architecture

Recurve is a multi-tenant subscription-analytics platform. The interesting part
is the data engineering: ingesting many companies' billing data into one
warehouse and guaranteeing a query can never leak across tenants.

```
 Marketing site + App (Next.js App Router, Vercel)
   ├─ (marketing): landing, pricing, /demo  ── SEO, OG, JSON-LD
   └─ (app): dashboard, onboarding ── Clerk auth → resolves tenant_id
                       │ calls
                       ▼
 Data API (FastAPI on Cloud Run, scale-to-zero)
   ├─ POST /connect      store encrypted Stripe restricted key, kick off ingest
   ├─ POST /run/{tenant} trigger that tenant's pipeline
   └─ GET  /metrics/...  serve aggregated, tenant-scoped metrics
                       │
                       ▼
 Pipeline:  dlt (per-tenant Stripe EL) → warehouse raw
            → dbt (staging → intermediate → marts, tenant_id everywhere, RLS)
            → churn model (scikit-learn) → mart_churn_scores
            orchestrated by Dagster (partition = tenant, fan-out)

 Warehouse:     DuckDB (local)  /  BigQuery (live, with Row Access Policies)
 Control plane: Postgres (tenants, connections[encrypted], users↔tenant)
```

## Stack (pinned versions in this scaffold)

| Layer          | Tech                                              |
| -------------- | ------------------------------------------------- |
| Frontend       | Next.js 16, React 19, TypeScript, Tailwind v4     |
| Auth           | Clerk (added in P0/P3)                            |
| Data API       | FastAPI on Cloud Run                              |
| Ingestion      | dlt 1.28                                          |
| Transformation | dbt-core 1.11 (dbt-duckdb local / dbt-bigquery)  |
| Orchestration  | Dagster 1.13 (tenant-partitioned)                |
| Churn model    | scikit-learn 1.9                                 |
| Warehouse      | DuckDB 1.5 (local) / BigQuery (live)             |
| Control plane  | Postgres 16                                      |
| Runtime        | Python 3.12 (uv-managed), Node 26, Docker (Colima)|

## Repo layout

```
recurve/
├── web/                       Next.js app (marketing + dashboard)
├── services/api/              FastAPI data API
├── pipeline/
│   ├── ingest/                dlt — Stripe → raw, per tenant
│   ├── transform/recurve/     dbt — staging → intermediate → marts
│   ├── orchestration/         Dagster — tenant-partitioned assets
│   └── ml/                    scikit-learn churn model
├── infra/postgres/            control-plane schema (init.sql)
├── docs/                      architecture, data model, brand
├── Dockerfile                 shared image for the Python services
├── docker-compose.yml         local stack (postgres + api + dagster)
└── pyproject.toml             uv workspace, pinned to Python 3.12
```

## Tenant isolation (the load-bearing guarantee)

- `tenant_id` on every raw row (stamped at ingest) and every dbt model.
- dbt tests assert no row lacks a tenant, and a "tenant B sees nothing of
  tenant A" check passes.
- BigQuery Row Access Policy keyed on `tenant_id` in the live warehouse.
- The API authorizes every request against the caller's tenant before
  returning a single row.

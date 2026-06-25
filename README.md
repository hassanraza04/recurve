# Recurve

**Know your recurring revenue cold.**

Recurve connects to a subscription business's Stripe account and turns raw
billing events into the metrics leadership actually runs on — MRR/ARR, the
MRR-movement waterfall, cohort retention, net revenue retention — plus a model
that flags the accounts about to churn. It's **multi-tenant**: many companies'
billing in one warehouse, with isolation guaranteed at the query layer.

It answers four questions with conviction, and every number is auditable back to
the rows:

> How much recurring revenue do we have? Is it growing? Where is it leaking?
> Who's about to leave?

---

## Status

🚧 **Scaffold.** The environment, repo structure, and reproducible local stack
are in place. Feature work follows the phased plan below.

- [x] **P0** — repo, design tokens, environment, reproducible stack, CI
- [ ] **P1** — multi-tenant dlt ingest + demo seeder + control-plane DB
- [ ] **P2** — dbt models, SCD2, tenant isolation, ≥20 tests
- [ ] **P3** — Dagster fan-out, FastAPI metrics, self-serve onboarding
- [ ] **P4** — the four dashboard screens
- [ ] **P5** — churn model + "Recurve's read"
- [ ] **P6** — marketing site, one-click demo, SEO
- [ ] **P7** — full audit, deploy, ship

## Architecture

See [docs/architecture.md](docs/architecture.md) for the full picture and
[docs/data_model.md](docs/data_model.md) for the dimensional model.

```
Next.js (web)  →  FastAPI (data API)  →  dlt → dbt → churn model
                                          orchestrated by Dagster (partition = tenant)
Warehouse: DuckDB (local) / BigQuery (live, Row Access Policies)
Control plane: Postgres (tenants, encrypted connections, users↔tenant)
```

## Local development

Requires [uv](https://docs.astral.sh/uv/), Node 20+, and a Docker runtime
(Docker Desktop or Colima).

```bash
# 1. Python environment (pinned to 3.12, isolated)
uv sync

# 2. Control-plane Postgres (creates the schema from infra/postgres/init.sql)
docker compose up -d --wait postgres

# 3. Data API
uv run uvicorn services.api.app.main:app --reload --port 8000
#    → http://localhost:8000/health  and docs at /docs

# 4. Web app
cd web && npm install && npm run dev
#    → http://localhost:3000

# Checks
uv run ruff check . && uv run pytest -q     # python
cd web && npm run lint && npm run build      # web
```

Copy `.env.example` to `.env` (root) and `web/.env.local` (web), and fill in the
blanks as each integration comes online.

## Repo layout

| Path                       | What                                         |
| -------------------------- | -------------------------------------------- |
| `web/`                     | Next.js app — marketing + dashboard          |
| `services/api/`            | FastAPI data API                             |
| `pipeline/ingest/`         | dlt — Stripe → raw, per tenant               |
| `pipeline/transform/`      | dbt — staging → intermediate → marts         |
| `pipeline/orchestration/`  | Dagster — tenant-partitioned assets          |
| `pipeline/ml/`             | scikit-learn churn model                     |
| `infra/postgres/`          | control-plane schema                         |
| `docs/`                    | architecture, data model, brand              |

---

Built by Hassan Raza.

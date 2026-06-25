# Transform (dbt)

Turns raw Stripe events into the metrics layer. Three layers:

- **staging** — clean/cast, one model per source table, `tenant_id` preserved.
- **intermediate** — the hard part: subscriptions → monthly periods → MRR
  movement type (`new` / `expansion` / `contraction` / `churn` / `reactivation`).
- **marts** — the §7 schema: `dim_customer` (SCD2 snapshot), `dim_plan`,
  `dim_date`, `fct_mrr_monthly`, `fct_invoice`, `mart_churn_scores`.

## Tenant isolation

Every model carries `tenant_id`. Custom dbt tests assert no row lacks a tenant
and that a "tenant B sees nothing of tenant A" check holds. The live warehouse
adds a BigQuery Row Access Policy keyed on `tenant_id`.

## Run locally

From this directory, with the env pointed at the local DuckDB warehouse:

```bash
uv run dbt deps
uv run dbt build --profiles-dir .
```

Models, snapshots and tests are written in **P2**.

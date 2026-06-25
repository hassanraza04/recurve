# Ingest (dlt)

Extract/load from Stripe into the raw warehouse, one tenant per run.

- `stripe_source.py` — the dlt source: which Stripe objects we pull and how
  they're keyed. Every row gets a `tenant_id`; loads merge (idempotent).
- `seed_billing.py` — generates the demo tenant's synthetic billing history so
  `/demo` and screenshots have something real to show.

Built in **P1**. Local destination is DuckDB; live is BigQuery.

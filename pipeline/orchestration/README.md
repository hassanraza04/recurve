# Orchestration (Dagster)

Runs the pipeline `ingest → dbt → churn`, **partitioned by tenant**. Each tenant
is a partition key; the schedule fans out across all tenants; new tenants are
added as dynamic partitions on connect. Freshness and asset checks land in P3.

## Run locally

```bash
cd pipeline/orchestration
uv run dagster dev -m recurve_orchestration.definitions
```

Then open the Dagster UI at http://localhost:3000 (asset bodies are stubbed until P3/P5).

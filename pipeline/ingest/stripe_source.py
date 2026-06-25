"""Stripe -> raw warehouse, via dlt. One tenant per run.

Scaffold only. The resources below name what we pull and how it's keyed; the
actual extraction (Stripe test-mode API, pagination, incremental cursors) is
built in P1. Two invariants are load-bearing and called out now so they don't
get lost later:

  1. tenant_id is stamped on EVERY row, by us, before it lands. The warehouse is
     multi-tenant; a row without a tenant is a bug a dbt test will catch.
  2. Loads are idempotent. Merge on the natural Stripe id (+ tenant_id) so a
     re-run updates in place instead of duplicating.
"""

from __future__ import annotations

import dlt

# The Stripe objects we need to reconstruct MRR, movement, retention and churn.
STRIPE_RESOURCES = (
    "customers",
    "subscriptions",
    "subscription_items",
    "invoices",
    "prices",
)


@dlt.source(name="stripe_raw")
def stripe_source(tenant_id: str, restricted_key: str):
    """Yield one dlt resource per Stripe object, each stamped with tenant_id.

    TODO(P1): pull from Stripe test mode with the tenant's restricted key,
    page through results, add incremental cursors on `created`, and merge on
    (tenant_id, id).
    """
    raise NotImplementedError("stripe extraction lands in P1")


def run_ingest(tenant_id: str, restricted_key: str, destination: str = "duckdb") -> None:
    """Entry point the API/Dagster will call to ingest one tenant.

    TODO(P1): build the dlt pipeline, set the destination (duckdb local /
    bigquery live), run the source, and record the run in ingest_runs.
    """
    raise NotImplementedError("ingest runner lands in P1")

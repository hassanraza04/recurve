"""Dagster definitions.

The orchestration shape is the interesting part and is fixed now even though the
asset bodies land in P3: the pipeline is **partitioned by tenant**. Each tenant
is a partition key; a run materializes ingest -> dbt -> churn for one tenant, and
the schedule fans out across all of them. New tenants are added as dynamic
partitions when they connect Stripe.
"""

from dagster import (
    AssetExecutionContext,
    Definitions,
    DynamicPartitionsDefinition,
    asset,
)

# one partition per tenant; added dynamically when a tenant connects
tenant_partitions = DynamicPartitionsDefinition(name="tenant")


@asset(partitions_def=tenant_partitions, group_name="ingest")
def stripe_raw(context: AssetExecutionContext) -> None:
    """Ingest one tenant's Stripe data via dlt. Body lands in P3."""
    raise NotImplementedError("ingest asset is implemented in P3")


@asset(
    partitions_def=tenant_partitions,
    group_name="transform",
    deps=[stripe_raw],
)
def dbt_marts(context: AssetExecutionContext) -> None:
    """Run dbt for one tenant (staging -> intermediate -> marts). Body lands in P3."""
    raise NotImplementedError("dbt asset is implemented in P3")


@asset(
    partitions_def=tenant_partitions,
    group_name="ml",
    deps=[dbt_marts],
)
def churn_scores(context: AssetExecutionContext) -> None:
    """Score one tenant's accounts into mart_churn_scores. Body lands in P5."""
    raise NotImplementedError("churn asset is implemented in P5")


defs = Definitions(assets=[stripe_raw, dbt_marts, churn_scores])

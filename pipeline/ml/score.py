"""Score one tenant's accounts into mart_churn_scores.

Scaffold only — built in P5. Output grain: one row per (tenant, customer,
score_date) with churn_probability, a risk_band, and top_features so the at-risk
screen can show *why* an account is flagged, not just a number.
"""

from __future__ import annotations


def score_tenant(tenant_id: str) -> None:
    """Load the model, score the tenant's active accounts, write mart_churn_scores.

    TODO(P5): pull current features for the tenant, predict probabilities,
    derive risk bands, attach per-account top features, upsert into the mart.
    """
    raise NotImplementedError("churn scoring lands in P5")

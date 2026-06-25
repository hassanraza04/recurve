"""Seed a demo tenant with realistic billing history.

The demo tenant is the single most important asset in the product — the
one-click `/demo` and every recruiter screenshot run on it. It needs 2-3 years
of plausible signups, upgrades, downgrades, churn and reactivation so cohorts
and the movement waterfall actually mean something. Generated, not scraped, so
it's safe to ship publicly.

Scaffold only — the generator lands in P1.
"""

from __future__ import annotations

DEMO_TENANT_SLUG = "demo"

# Knobs the generator will respect so the numbers look like a real SaaS, not noise.
DEMO_CONFIG = {
    "months_of_history": 30,
    "starting_customers": 40,
    "monthly_signups": (8, 22),  # range
    "monthly_logo_churn_pct": (0.015, 0.035),
    "expansion_rate_pct": (0.02, 0.05),
    "plans": [
        {"tier": "starter", "unit_amount": 4900, "interval": "month"},
        {"tier": "growth", "unit_amount": 14900, "interval": "month"},
        {"tier": "scale", "unit_amount": 49900, "interval": "month"},
    ],
}


def seed_demo_tenant() -> None:
    """Create the demo tenant and write its synthetic billing history to raw.

    TODO(P1): generate customers/subscriptions/invoices with the config above,
    stamp tenant_id, and land them through the same raw tables dlt writes to,
    so the demo flows through the identical dbt models as a real tenant.
    """
    raise NotImplementedError("demo seeder lands in P1")


if __name__ == "__main__":
    seed_demo_tenant()

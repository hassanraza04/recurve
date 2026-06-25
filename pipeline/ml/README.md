# Churn model (scikit-learn)

Flags the accounts about to leave, with a reason.

- `train.py` — fit on leakage-free features; evaluate with **precision@k** (the
  accounts a CS team can realistically call), not a vanity AUC.
- `score.py` — score a tenant's active accounts into `mart_churn_scores`
  (`churn_probability`, `risk_band`, `top_features`).

Runs as a per-tenant Dagster asset. Built in **P5**.

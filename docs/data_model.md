# Data model

Kimball-style dimensional model. Every mart carries `tenant_id`.

## Marts

```
dim_customer     (tenant_id, customer_key, stripe_id, company, plan_tier,
                  signup_date, country, is_active, valid_from, valid_to)
                  -- SCD2 via dbt snapshot

dim_plan         (tenant_id, plan_key, name, interval, unit_amount, tier)

dim_date         (date_key, date, month, quarter, year, ...)

fct_mrr_monthly  (tenant_id, customer_key, month_date_key, mrr, movement_type,
                  prev_mrr, mrr_delta)
                  -- grain: tenant × customer × month
                  -- movement_type ∈ {new, expansion, contraction, churn, reactivation}

fct_invoice      (tenant_id, invoice_key, customer_key, date_key, amount,
                  status, paid)

mart_churn_scores (tenant_id, customer_key, score_date, churn_probability,
                   risk_band, top_features)
```

## Metrics served from the marts

MRR, ARR, Net New MRR, MRR-movement breakdown, Logo Churn %, Gross/Net Revenue
Retention, ARPA, LTV, Quick Ratio, cohort retention %.

## Data-quality contract (dbt tests)

- unique / not-null / relationships on every key.
- **no row without a tenant_id** (custom test).
- **tenant isolation**: a query scoped to tenant B returns nothing of tenant A.
- **MRR movements reconcile**: the sum of movement components equals the net
  MRR delta for each tenant × month.
- **no negative MRR**: contraction/churn clip to zero, never below.

Built in **P2**. The intent is that any number on screen can be traced back to
the rows that produced it.

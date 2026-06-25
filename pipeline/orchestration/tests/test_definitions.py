def test_defs_load_with_tenant_partitioned_assets():
    from recurve_orchestration.definitions import defs

    keys = {k.to_user_string() for k in defs.resolve_asset_graph().get_all_asset_keys()}
    assert keys == {"stripe_raw", "dbt_marts", "churn_scores"}

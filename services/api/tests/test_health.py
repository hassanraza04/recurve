from fastapi.testclient import TestClient

from services.api.app.main import app

client = TestClient(app)


def test_health_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_connect_is_stubbed_until_p3():
    # the real flow is built in P3; until then it must not pretend to work
    resp = client.post(
        "/v1/connect",
        json={"tenant_id": "t_1", "restricted_key": "rk_test_1234567890", "mode": "test"},
    )
    assert resp.status_code == 501

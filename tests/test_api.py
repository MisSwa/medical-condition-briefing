import app.main as main_module

_FAKE_STATE = {
    "condition": "asthma",
    "pubmed_results": [],
    "trial_results": [],
    "brief": {
        "condition": "asthma",
        "standard_of_care": ["Inhaled corticosteroids"],
        "emerging_treatments": ["Biologic therapy"],
        "key_organizations": ["Example Hospital"],
        "sources": ["pmid:12345678"],
    },
}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_brief_returns_correct_shape(client, monkeypatch):
    monkeypatch.setattr(main_module.briefing_graph, "invoke", lambda _: _FAKE_STATE)
    response = client.post("/brief", json={"condition": "asthma"})
    assert response.status_code == 200
    body = response.json()
    assert body["condition"] == "asthma"
    assert isinstance(body["standard_of_care"], list)
    assert isinstance(body["emerging_treatments"], list)
    assert isinstance(body["key_organizations"], list)
    assert isinstance(body["sources"], list)


def test_brief_empty_condition_returns_422(client):
    response = client.post("/brief", json={"condition": ""})
    assert response.status_code == 422


def test_brief_whitespace_condition_returns_422(client):
    response = client.post("/brief", json={"condition": "   "})
    assert response.status_code == 422


def test_brief_upstream_failure_returns_503(client, monkeypatch):
    def raise_error(_):
        raise RuntimeError("Claude API unavailable")

    monkeypatch.setattr(main_module.briefing_graph, "invoke", raise_error)
    response = client.post("/brief", json={"condition": "asthma"})
    assert response.status_code == 503
    assert "Brief generation failed" in response.json()["detail"]

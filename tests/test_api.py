def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_brief_stub(client):
    response = client.post("/brief", json={"condition": "asthma"})
    assert response.status_code == 200
    body = response.json()
    assert body["condition"] == "asthma"
    assert isinstance(body["standard_of_care"], list)
    assert isinstance(body["emerging_treatments"], list)
    assert isinstance(body["key_organizations"], list)
    assert isinstance(body["sources"], list)

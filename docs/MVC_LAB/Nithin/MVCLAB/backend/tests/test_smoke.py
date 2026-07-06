def test_client_fixture_wires_Nithin_as_current_user(client, Nithin):
    r = client.get("/api/tasks/")
    assert r.status_code == 200
    assert r.json() == []

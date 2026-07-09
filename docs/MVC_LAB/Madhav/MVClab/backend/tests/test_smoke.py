def test_client_fixture_wires_ronaldo_as_current_user(client, ronaldo):
    r = client.get("/tasks/")
    assert r.status_code == 200
    assert r.json() == []  # Ronaldo has no tasks yet
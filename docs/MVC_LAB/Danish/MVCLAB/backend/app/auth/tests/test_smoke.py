def test_client_fixture_wires_Eshwaryadav_as_current_user(client, Eshwaryadav):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []  # Assuming no tasks exist for Eshwaryadav initially
def test_client_fixture_wires_alice_as_current_user(client, alice):
    """Smoke test to verify that the client fixture correctly authenticates Alice."""
    # Act: Request the tasks endpoint (which expects an authenticated user context)
    response = client.get("/tasks/")
    
    # Assert: We expect a successful response, and an empty list since Alice has no tasks yet
    assert response.status_code == 200
    assert response.json() == []
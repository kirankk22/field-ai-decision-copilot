def test_health_endpoint(client):
    """
    Verify that the FastAPI application is alive
    and exposes the expected health endpoint.
    """

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
def test_homepage(client):
    """Test the homepage works (HTTP status 200 OK)"""
    resp = client.get("/")
    assert resp.status_code == 200

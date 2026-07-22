def test_booking_page_for_existing_competition(logged_in_client):
    """A logged in user can view the booking page for a real competition."""
    resp = logged_in_client.get("/book/Spring Festival")
    assert resp.status_code == 200
    body = resp.data.decode()
    assert "Spring Festival" in body
    assert "25" in body


def test_booking_page_for_unknown_competition_returns_404(logged_in_client):
    """A logged in user cannot view a booking page for a competition that
    doesn't exist."""
    resp = logged_in_client.get("/book/Not A Real Competition")
    assert resp.status_code == 404


def test_booking_page_requires_login(client):
    """A user who isn't logged in is redirected away instead of crashing."""
    resp = client.get("/book/Spring Festival")
    assert resp.status_code == 302

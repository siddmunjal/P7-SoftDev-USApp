def test_login_with_valid_email(client):
    """A user can login by typing a valid email in the form on the homepage."""
    resp = client.post(
        "/login", data={"email": "john@simplylift.co"}, follow_redirects=True
    )
    # Redirected to the summary page
    assert resp.request.path == "/summary"
    assert resp.status_code == 200
    body = resp.data.decode()
    assert "john@simplylift.co" in body
    assert "13" in body


def test_login_with_unknown_email_returns_401(client):
    """issue #1: an unknown email must not crash the app, it must return 401."""
    resp = client.post(
        "/login", data={"email": "not-a-real-club@example.com"}, follow_redirects=True
    )
    assert resp.status_code == 401


def test_login_with_missing_email_field_returns_401(client):
    """Submitting the form with no email at all should also be rejected cleanly."""
    resp = client.post("/login", data={})
    assert resp.status_code == 401


def test_summary_requires_login(client):
    """Visiting /summary without being logged in redirects to the homepage
    instead of crashing."""
    resp = client.get("/summary")
    assert resp.status_code == 302


def test_logout(logged_in_client):
    """Logging out clears the session and redirects to the homepage."""
    resp = logged_in_client.get("/logout", follow_redirects=True)
    assert resp.status_code == 200
    assert resp.request.path == "/"
    assert logged_in_client.get("/summary").status_code == 302

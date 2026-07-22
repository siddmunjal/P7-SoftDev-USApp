def _book(client, competition, spots):
    return client.post("/book", data={"competition": competition, "spots": spots})


def test_successful_booking_shows_confirmation(logged_in_client):
    """A valid booking shows a confirmation message."""
    resp = _book(logged_in_client, "Spring Festival", "3")
    assert resp.status_code == 200
    assert "booking complete" in resp.data.decode().lower()


def test_successful_booking_deducts_points(logged_in_client):
    """Points for the club go down by the number of spots booked."""
    resp = _book(logged_in_client, "Spring Festival", "3")
    body = resp.data.decode()
    # Club started with 13 points, spent 3 -> 10 left
    assert "10" in body


def test_cannot_book_more_spots_than_points_available(logged_in_client):
    """issue #2: a club cannot spend more points than it has."""
    logged_in_client.post(
        "/login", data={"email": "admin@irontemple.com"}, follow_redirects=True
    )
    resp = _book(logged_in_client, "Spring Festival", "5")
    assert resp.status_code == 403


def test_cannot_book_more_than_12_spots(logged_in_client):
    """issue #3: a club cannot book more than 12 spots in a single
    competition, even if it has enough points."""
    resp = _book(logged_in_client, "Spring Festival", "13")
    assert resp.status_code == 403


def test_cannot_book_spots_in_a_past_competition(logged_in_client):
    """issue #4: a club cannot book spots for a competition that has
    already happened."""
    resp = _book(logged_in_client, "Fall Classic", "1")
    assert resp.status_code == 403


def test_cannot_book_more_spots_than_available_in_competition(logged_in_client):
    """A club cannot book more spots than remain in the competition, even
    when it has enough points and stays under the 12-spot cap."""
    # Summer Sprint is in the future and only has 2 spots left.
    resp = _book(logged_in_client, "Summer Sprint", "3")
    assert resp.status_code == 403


def test_cannot_book_for_unknown_competition(logged_in_client):
    resp = _book(logged_in_client, "Not A Real Competition", "1")
    assert resp.status_code == 404


def test_booking_requires_login(client):
    resp = client.post("/book", data={"competition": "Spring Festival", "spots": "1"})
    assert resp.status_code == 302

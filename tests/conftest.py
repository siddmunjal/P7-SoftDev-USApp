from datetime import datetime, timedelta

import pytest

from server import app as flask_app

PAST_DATE = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
FUTURE_DATE = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")


def mock_clubs():
    """Static data to mock clubs. Returns a fresh list/dicts every call, mirroring
    the fact that provider.get_clubs() re-reads the JSON file each time."""
    return [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
    ]


def mock_competitions():
    """Static data to mock competitions: one in the future, one in the past."""
    return [
        {
            "name": "Spring Festival",
            "date": FUTURE_DATE,
            "spotsAvailable": "25",
        },
        {
            "name": "Fall Classic",
            "date": PAST_DATE,
            "spotsAvailable": "13",
        },
        {
            "name": "Summer Sprint",
            "date": FUTURE_DATE,
            "spotsAvailable": "2",
        },
    ]


@pytest.fixture(autouse=True)
def mock_data_provider(monkeypatch):
    """
    This fixture is automatically used in every test function.

    We patch `server.get_clubs` / `server.get_competitions` (and the save_*
    equivalents), because that's where those functions are used, not where
    they're defined.
    """
    saved = {"clubs": None, "competitions": None}

    monkeypatch.setattr("server.get_clubs", mock_clubs)
    monkeypatch.setattr("server.get_competitions", mock_competitions)
    monkeypatch.setattr("server.save_clubs", lambda clubs: saved.__setitem__("clubs", clubs))
    monkeypatch.setattr(
        "server.save_competitions", lambda comps: saved.__setitem__("competitions", comps)
    )

    return saved


@pytest.fixture
def app():
    flask_app.config.update({"TESTING": True})
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def logged_in_client(client):
    """A test client that is already logged in as Simply Lift (13 points)."""
    client.post("/login", data={"email": "john@simplylift.co"}, follow_redirects=True)
    return client

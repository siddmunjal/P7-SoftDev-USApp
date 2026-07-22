import pytest

from server import app as flask_app


def mock_clubs():
    """Static data to mock clubs. Returns a fresh list/dicts every call, mirroring
    the fact that provider.get_clubs() re-reads the JSON file each time."""
    return [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
    ]


def mock_competitions():
    """Static data to mock competitions"""
    return [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "spotsAvailable": "25",
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "spotsAvailable": "13",
        },
    ]


@pytest.fixture(autouse=True)
def mock_data_provider(monkeypatch):
    """
    This fixture is automatically used in every test function.

    We patch `server.get_clubs` / `server.get_competitions`, because that's
    where those functions are used, not where they're defined.
    """
    monkeypatch.setattr("server.get_clubs", mock_clubs)
    monkeypatch.setattr("server.get_competitions", mock_competitions)


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

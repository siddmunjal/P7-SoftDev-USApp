import json

import provider


def test_get_clubs_reads_real_json_file():
    """Clubs are loaded from clubs.json."""
    clubs = provider.get_clubs()
    assert isinstance(clubs, list)
    assert any(c["email"] == "john@simplylift.co" for c in clubs)


def test_get_competitions_reads_real_json_file():
    """Competitions are loaded from competitions.json."""
    competitions = provider.get_competitions()
    assert isinstance(competitions, list)
    assert any(c["name"] == "Spring Festival" for c in competitions)


def test_save_clubs_persists_and_is_read_back(tmp_path, monkeypatch):
    """save_clubs() writes back to disk, and get_clubs() sees the update
    (this is what fixes issue #5 - points weren't being persisted)."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "clubs.json").write_text(json.dumps({"clubs": []}))

    # Path(__file__).parent / DATA_FOLDER: an absolute DATA_FOLDER overrides
    # the left-hand side entirely, so this fully isolates the test from the
    # real data/ folder.
    monkeypatch.setattr(provider, "DATA_FOLDER", str(data_dir))

    new_clubs = [{"name": "Test Club", "email": "test@club.co", "points": "7"}]
    provider.save_clubs(new_clubs)

    assert provider.get_clubs() == new_clubs


def test_save_competitions_persists_and_is_read_back(tmp_path, monkeypatch):
    """save_competitions() writes back to disk, and get_competitions() sees
    the update."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "competitions.json").write_text(json.dumps({"competitions": []}))

    monkeypatch.setattr(provider, "DATA_FOLDER", str(data_dir))

    new_competitions = [
        {"name": "Test Comp", "date": "2030-01-01 10:00:00", "spotsAvailable": "5"}
    ]
    provider.save_competitions(new_competitions)

    assert provider.get_competitions() == new_competitions

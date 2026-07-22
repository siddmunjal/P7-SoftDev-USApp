import json
from pathlib import Path

DATA_FOLDER = "data"


def _json_from_file(filename, key):
    """Helper method - loads JSON from 'filename' and return whatever is at the 'key'"""
    filepath = Path(__file__).parent / DATA_FOLDER / filename
    with open(filepath) as fp:
        data = json.load(fp)
        return data[key]


def get_clubs():
    """Load clubs from JSON"""
    return _json_from_file("clubs.json", "clubs")


def get_competitions():
    """Load competitions from JSON"""
    return _json_from_file("competitions.json", "competitions")


def _save_json_to_file(filename, key, data):
    """Helper method - persists 'data' under 'key' back into 'filename'"""
    filepath = Path(__file__).parent / DATA_FOLDER / filename
    with open(filepath) as fp:
        contents = json.load(fp)
    contents[key] = data
    with open(filepath, "w") as fp:
        json.dump(contents, fp, indent=4)


def save_clubs(clubs):
    """Persist the clubs list (e.g. after a points update)"""
    _save_json_to_file("clubs.json", "clubs", clubs)


def save_competitions(competitions):
    """Persist the competitions list (e.g. after a booking)"""
    _save_json_to_file("competitions.json", "competitions", competitions)

# gudlift-registration

### Why

This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

### Getting Started

This project uses the following technologies:

* Python v3.x+
* [Flask](https://flask.palletsprojects.com/)
* [Virtual environment](https://docs.python.org/3/library/venv.html)


### Installation

- Clone the repository and create a new virtual (`python -m venv <VENV_FOLDER>`)

- Make sure the virtual environment you created is active

- Install the requirements based on the `requirements.txt` file: `pip install -r requirements.txt`

- Run the application with `python server.py`. The app will start and display in the terminal a link where you can access it (locally) using your browser.

### Current setup

The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). They live in the `data` folder.
    
* `competitions.json` - list of competitions
* `clubs.json` - list of clubs with relevant information. Inspect this file to find email addresses you can use to login.

Bookings made through the app (`POST /book`) are written back to these JSON files via
`provider.save_clubs()` / `provider.save_competitions()`, so a club's points and a
competition's remaining spots persist across requests and server restarts.

### Routes

| Route | Method | Auth | Notes |
| --- | --- | --- | --- |
| `/` | GET | none | Login form |
| `/login` | POST | none | `401` if the email doesn't match a club |
| `/summary` | GET | logged in | Club's dashboard |
| `/book/<competition>` | GET | logged in | `404` if the competition doesn't exist |
| `/book` | POST | logged in | Booking form submission; `400` on invalid `spots`, `403` if the booking breaks any rule below, `404` if the competition doesn't exist |
| `/clubs` | GET | none | Public points board - every club's name and points balance |
| `/logout` | GET | logged in | Clears the session |

Booking rules enforced on `POST /book` (all return `403` on violation):
1. The competition must not be in the past.
2. A club may not book more than 12 spots in a single competition.
3. A club may not spend more points than it has.
4. A club may not book more spots than the competition has available.

### Testing

The project uses [pytest](https://docs.pytest.org/), plus [pytest-cov](https://pytest-cov.readthedocs.io/) for coverage.

```
pip install -r requirements-dev.txt
pytest tests/ -v --cov=. --cov-report=term-missing
flake8 server.py provider.py tests/
```

The test suite mocks `server.get_clubs` / `server.get_competitions` / `server.save_clubs` /
`server.save_competitions` (see `tests/conftest.py`) so tests never touch the real `data/*.json`
files.

### QA build history

Fixed on top of the original POC (see `tests/README.md` for the full test plan), one branch per
issue, following the branch naming convention in this README's Annex:

* `bug/1-unknown-email-crashes-app` - unknown email now returns 401 instead of crashing
* `bug/2-clubs-overspend-points` - a club can no longer spend more points than it has
* `bug/3-more-than-12-spots` - a club can no longer book more than 12 spots per competition
* `bug/4-book-in-past-competitions` - a club can no longer book a competition that's already happened
* `bug/5-point-updates-not-reflected` - bookings are now persisted to the JSON data files
* `feature/6-points-board-system` - added the public `/clubs` points board

All of the above are merged into `qa` for review.


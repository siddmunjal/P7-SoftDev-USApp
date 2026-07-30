### Current setup

The app is powered by JSON files in the `data` folder — `clubs.json` and
`competitions.json`. Check `clubs.json` for an email address to log in with.

### Testing

Uses pytest + pytest-cov for coverage, and flake8 for style.

1. Check out this branch: `git checkout qa`
2. Create a virtual environment: `python -m venv venv`
3. Activate it:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements-dev.txt`
5. Run the tests: `pytest tests/ -v --cov=. --cov-report=term-missing`
6. Check style: `flake8 server.py provider.py tests/`

Tests mock `server.get_clubs` / `server.get_competitions` / `server.save_clubs` /
`server.save_competitions` (see `tests/conftest.py`), so running them never touches
the real `data/*.json` files.

### Notes on this build

- Bookings now persist: `provider.py` writes updated points/spots back to the JSON
  files after a booking, so they survive a restart instead of only living in memory.
- A booking is rejected (with the relevant error code) if the competition has
  already happened, the club is trying to book more than 12 spots, it doesn't have
  enough points, or the competition doesn't have that many spots left.
- Every club can now be viewed publicly at `/clubs`, without logging in.


from datetime import datetime

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for

from provider import get_clubs, get_competitions, save_clubs, save_competitions

MAX_SPOTS_PER_CLUB = 12

app = Flask(__name__)
# You should change the secret key in production!
app.secret_key = "something_special"


def _find_club_by_email(clubs, email):
    matches = [club for club in clubs if club["email"] == email]
    return matches[0] if matches else None


def _find_competition_by_name(competitions, name):
    matches = [comp for comp in competitions if comp["name"] == name]
    return matches[0] if matches else None


def _competition_is_in_the_past(competition):
    comp_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
    return comp_date < datetime.now()


@app.route("/")
def index():
    """Homepage"""
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    """Use the session object to store the club information across requests"""

    clubs = get_clubs()
    email = request.form.get("email", "")

    club = _find_club_by_email(clubs, email)
    if club is None:
        # Unknown email: reject the login instead of crashing (issue #1)
        abort(401)

    session["club"] = club

    return redirect(url_for("summary"))


@app.route("/summary")
def summary():
    """Custom "homepage" for logged in users"""

    club = session.get("club")
    if club is None:
        return redirect(url_for("index"))

    competitions = get_competitions()

    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>")
def book(competition):
    """Book spots in a competition page"""
    club = session.get("club")
    if club is None:
        return redirect(url_for("index"))

    competitions = get_competitions()
    found_competition = _find_competition_by_name(competitions, competition)

    if found_competition is None:
        abort(404)

    return render_template("booking.html", club=club, competition=found_competition)


@app.route("/book", methods=["POST"])
def book_spots():
    """This page is only accessible through a POST request (form validation)"""
    club = session.get("club")
    if club is None:
        return redirect(url_for("index"))

    clubs = get_clubs()
    competitions = get_competitions()

    competition = _find_competition_by_name(competitions, request.form.get("competition", ""))
    if competition is None:
        abort(404)

    # Always work off the freshly-loaded club record, since points may have
    # changed since the user logged in.
    current_club = _find_club_by_email(clubs, club["email"])
    if current_club is None:
        abort(401)

    if _competition_is_in_the_past(competition):
        # Can't book spots in a competition that has already happened (issue #4)
        abort(403)

    spots_required = int(request.form["spots"])

    if spots_required > MAX_SPOTS_PER_CLUB:
        # Clubs may not book more than 12 spots per competition (issue #3)
        abort(403)

    if spots_required > int(current_club["points"]):
        # Clubs may not spend more points than they have (issue #2)
        abort(403)

    if spots_required > int(competition["spotsAvailable"]):
        # Can't book more spots than are available in the competition
        abort(403)

    competition["spotsAvailable"] = str(int(competition["spotsAvailable"]) - spots_required)
    current_club["points"] = str(int(current_club["points"]) - spots_required)

    # Persist both updates so they're reflected on future requests (issue #5)
    save_competitions(competitions)
    save_clubs(clubs)

    session["club"] = current_club

    flash("Great-booking complete!")
    return render_template("welcome.html", club=current_club, competitions=competitions)


@app.route("/logout")
def logout():
    """We delete session data in order to log the user out"""
    session.pop("club", None)
    return redirect(url_for("index"))


@app.errorhandler(401)
def unauthorized(error):
    message = "That email address isn't recognised."
    return render_template("error.html", code=401, message=message), 401


@app.errorhandler(403)
def forbidden(error):
    message = "That booking isn't allowed."
    return render_template("error.html", code=403, message=message), 403


@app.errorhandler(404)
def not_found(error):
    message = "We couldn't find that competition."
    return render_template("error.html", code=404, message=message), 404


if __name__ == "__main__":
    app.run(debug=True)

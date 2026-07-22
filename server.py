from flask import Flask, abort, flash, redirect, render_template, request, session, url_for

from provider import get_clubs, get_competitions

app = Flask(__name__)
# You should change the secret key in production!
app.secret_key = "something_special"


def _find_club_by_email(clubs, email):
    matches = [club for club in clubs if club["email"] == email]
    return matches[0] if matches else None


def _find_competition_by_name(competitions, name):
    matches = [comp for comp in competitions if comp["name"] == name]
    return matches[0] if matches else None


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

    competitions = get_competitions()

    competition = _find_competition_by_name(competitions, request.form.get("competition", ""))
    if competition is None:
        abort(404)

    spots_required = int(request.form["spots"])
    competition["spotsAvailable"] = int(competition["spotsAvailable"]) - spots_required
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/logout")
def logout():
    """We delete session data in order to log the user out"""
    session.pop("club", None)
    return redirect(url_for("index"))


@app.errorhandler(401)
def unauthorized(error):
    message = "That email address isn't recognised."
    return render_template("error.html", code=401, message=message), 401


@app.errorhandler(404)
def not_found(error):
    message = "We couldn't find that competition."
    return render_template("error.html", code=404, message=message), 404


if __name__ == "__main__":
    app.run(debug=True)

import json
from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, url_for, abort


def load_clubs():
    with open("clubs.json") as file:
        return json.load(file)["clubs"]


def load_competitions():
    with open("competitions.json") as file:
        return json.load(file)["competitions"]


app = Flask(__name__)
app.config["SECRET_KEY"] = "something_special"

clubs = load_clubs()
competitions = sorted(load_competitions(), key=lambda c: c["date"], reverse=True)
date_format = "%Y-%m-%d %H:%M:%S"
past_competitions = [c for c in competitions if datetime.strptime(c["date"], date_format) < datetime.now()]
future_competitions = [c for c in competitions if datetime.strptime(c["date"], date_format) > datetime.now()]


@app.errorhandler(403)
def forbidden(e):
    return render_template("error_pages/403.html"), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error_pages/404.html"), 404


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/show_summary/", methods=["POST"])
def show_summary():
    try:
        club_found = [c for c in clubs if c["email"] == request.form["email"]][0]  # type:ignore
    except IndexError:
        flash("Sorry, that email wasn't found.")
        return redirect(url_for("index"))
    return render_template(
        "welcome.html",
        club=club_found,
        competitions=competitions,
        future_competitions=future_competitions
        )


@app.route("/book/<competition>/<club>/")
def book(competition, club):
    try:
        club_found = [c for c in clubs if c["name"] == club][0]
        competition_found = [c for c in competitions if c["name"] == competition][0]
    except IndexError:
        abort(404)
    if competition_found in past_competitions:
        abort(403)
    return render_template("booking.html", club=club_found, competition=competition_found)


@app.route("/purchase_places/", methods=["POST"])
def purchase_places():

    club_found = [c for c in clubs if c["name"] == request.form["club"]][0]  # type:ignore
    competition_found = [c for c in competitions if c["name"] == request.form["competition"]][0]  # type:ignore
    places_purchased = int(request.form["places"])  # type:ignore

    if places_purchased < 0:
        flash("You cannot book a negative number of places.")
        return redirect(url_for("book", competition=competition_found["name"], club=club_found["name"]))

    elif places_purchased > competition_found["numberOfPlaces"]:
        flash(f"You cannot buy so many places. There are only {competition_found['numberOfPlaces']} places left.")
        return redirect(url_for("book", competition=competition_found["name"], club=club_found["name"]))

    elif club_found["points"] < places_purchased:
        flash(f"You cannot buy so many places. You only have {club_found['points']} points.")
        return redirect(url_for("book", competition=competition_found["name"], club=club_found["name"]))

    elif competition_found["name"] in club_found["competitions"]:
        if club_found["competitions"][competition_found["name"]] + places_purchased > 12:
            flash("You can book 12 places max per competition.")
            return redirect(url_for("book", competition=competition_found["name"], club=club_found["name"]))

    competition_found["numberOfPlaces"] = competition_found["numberOfPlaces"] - places_purchased
    club_found["points"] = club_found["points"] - places_purchased

    if competition_found["name"] in club_found["competitions"]:
        club_found["competitions"][competition_found["name"]] = (
            club_found["competitions"][competition_found["name"]] + places_purchased
            )
    else:
        club_found["competitions"][competition_found["name"]] = places_purchased

    flash("Great-booking complete!")
    return render_template(
        "welcome.html",
        club=club_found,
        competitions=competitions,
        future_competitions=future_competitions
        )


# TODO: Add route for points display


@app.route("/logout/")
def logout():
    return redirect(url_for("index"))

import json

from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    with open("clubs.json") as file:
        return json.load(file)["clubs"]


def load_competitions():
    with open("competitions.json") as file:
        return json.load(file)["competitions"]


app = Flask(__name__)
app.config["SECRET_KEY"] = "something_special"

competitions = load_competitions()
clubs = load_clubs()


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
    return render_template("welcome.html", club=club_found, competitions=competitions)


@app.route("/book/<competition>/<club>/")
def book(competition, club):
    club_found = [c for c in clubs if c["name"] == club][0]
    competition_found = [c for c in competitions if c["name"] == competition][0]
    if club_found and competition_found:
        return render_template("booking.html", club=club_found, competition=competition_found)
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchase_places/", methods=["POST"])
def purchase_places():
    club_found = [c for c in clubs if c["name"] == request.form["club"]][0]  # type:ignore
    competition_found = [c for c in competitions if c["name"] == request.form["competition"]][0]  # type:ignore
    places_purchased = int(request.form["places"])  # type:ignore
    competition_found["numberOfPlaces"] = int(competition_found["numberOfPlaces"]) - places_purchased
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club_found, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout/")
def logout():
    return redirect(url_for("index"))

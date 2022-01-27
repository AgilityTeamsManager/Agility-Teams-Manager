#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROGESCO Teams.

Classements par équipe pour PROGESCO.
"""
import _csv
import csv
import hashlib
import os

from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)
users: dict[str, str] = {}
with open("data/users.csv") as f:
    passwords_file: _csv.reader = csv.reader(f)
    for row in passwords_file:
        users[row[0]] = row[1]

app.secret_key = os.environ["SECRET_KEY"]


@app.route("/login", methods=["GET", "POST"])
def index():
    """
    Main app page.

    Home screen and app page.
    """
    if request.method == "POST":
        # Check password
        if request.form["user"] in users:
            if hashlib.sha256(request.form["password"].encode()).hexdigest() == users[request.form["user"]]:
                session["auth"] = "true"
                return redirect("/app")
            else:
                return render_template("login.html", error="Mauvais mot de passe")
        else:
            return render_template("login.html", error="Utilisateur inconnu")
    return render_template("login.html")


@app.route("/manifest.json")
def manifest():
    """
    Manifest file.

    Redirects to static path.
    """
    return redirect("/static/manifest.json", 301)


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)

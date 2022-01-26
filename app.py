#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROGESCO Teams.

Classements par équipe pour PROGESCO.
"""
from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route("/login")
def index():
    """
    Main app page.

    Home screen and app page.
    """
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

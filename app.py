#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROGESCO Teams.

Classements par équipe pour PROGESCO.
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    """
    Main app page.

    Home screen and app page.
    """
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROGESCO Teams.

Classements par équipe pour PROGESCO.
"""
import _csv
import csv
import email.mime.multipart
import email.mime.text
import hashlib
import os
import smtplib
import uuid

from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)
users: dict[str, str] = {}
with open("data/users.csv") as f:
    passwords_file: _csv.reader = csv.reader(f)
    for row in passwords_file:
        users[row[0]] = row[1]

smtp_server: smtplib.SMTP_SSL = smtplib.SMTP_SSL("smtp.gmail.com", 465)
smtp_server.login("progesco.teams@gmail.com", os.environ["SECRET_GMAIL"])

signups: dict[str, dict[str, str]] = {}

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


@app.route("/account/signup/<uuid:id_confirm>")
def signup_confirm(id_confirm):
    """
    Confirm signup.
    """
    


@app.route("/account/signup", methods=["POST"])
def signup():
    """
    Signup.

    Send an email.
    """
    random_uuid: str = uuid.uuid4().hex
    signups[random_uuid] = {"user": request.form["user"], "password": hashlib.sha256(request.form["password"].encode()).hexdigest()}
    mail = email.mime.multipart.MIMEMultipart("alternative")
    mail["Subject"] = "PROGESCO Teams - Confirmer l'inscription"
    mail["From"] = "progesco.teams@gmail.com"
    mail["To"] = request.form["user"]
    confirm_url: str = request.url_root + "account/signup/" + random_uuid
    mail.attach(email.mime.text.MIMEText(f"Suivez ce lien pour confirmer votre inscription : {confirm_url}", "plain"))
    with open("signup_mail.html") as file:
        mail.attach(email.mime.text.MIMEText(file.read(), "html"))
    smtp_server.sendmail("progesco.teams@gmail.com", request.form["user"], mail.as_string())
    return render_template("signup.html")


@app.route("/manifest.json")
def manifest():
    """
    Manifest file.

    Redirects to static path.
    """
    return redirect("/static/manifest.json", 301)


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)

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

from flask import abort, Flask, render_template, redirect, request, session

app = Flask(__name__)
users: dict[str, str] = {}
with open("data/users.csv") as f:
    passwords_file: _csv.reader = csv.reader(f)
    for row in passwords_file:
        users[row[0]] = row[1]

signups: dict[str, dict[str, str]] = {}
password_resets: dict[str, str] = {}

app.secret_key = os.environ["SECRET_KEY"]


def send_mail(to: str, subject: str, message: str, mail_message: str, redirect: str, button: str) -> None:
    """
    Send a PROGESCO Teams mail.

    :param str to: Destination address.
    :param str subject: Mail subject.
    :param str message: Text message.
    :param str mail_message: Message for HTML part.
    :param str redirect: Redirect link in mail.
    :param str button: Button's text.
    :return: Nothing.
    :rtype: None
    """
    mail: email.mime.multipart.MIMEMultipart = email.mime.multipart.MIMEMultipart("alternative")
    mail["Subject"] = subject
    mail["From"] = "PROGESCO Teams<progesco.teams@gmail.com>"
    mail["To"] = to
    mail.attach(email.mime.text.MIMEText(message.format(redirect=redirect), "plain"))
    with open("mail.html") as file_object:
        mail_html: str = file_object.read().replace("@message", mail_message).replace("@link", redirect).replace("@button", button)
        print(mail_html)
        mail.attach(email.mime.text.MIMEText(mail_html, "html"))
    smtp_server: smtplib.SMTP_SSL = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp_server.login("progesco.teams@gmail.com", os.environ["SECRET_GMAIL"])
    smtp_server.sendmail("progesco.teams@gmail.com", to, mail.as_string())
    smtp_server.close()


@app.route("/")
def index():
    """
    Main page.

    Redirects to app or login screen.
    """
    if "auth" in session and session["auth"] == "true":
        return redirect("/app")
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
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
    entry: dict[str, str] = signups[str(id_confirm)]
    print(entry)
    if entry["user"] in users:
        return render_template("login.html", error=f"Le compte {entry['user']} existe dèjà.")
    # Add to CSV file
    with open("data/users.csv", "a") as file:
        writer: _csv.writer = csv.writer(file)
        hashed: str = entry["password"]
        writer.writerow([entry["user"], hashed])
        users[entry["user"]] = hashed
    return redirect("/login?message=Inscription réussie")


@app.route("/account/signup", methods=["POST"])
def signup():
    """
    Signup.

    Send an email.
    """
    if request.form["user"] in users:
        return render_template("login.html", error=f"Le compte {request.form['user']} existe dèjà.")
    random_uuid: str = str(uuid.uuid4())
    signups[random_uuid] = {"user": request.form["user"], "password": hashlib.sha256(request.form["password"].encode()).hexdigest()}
    send_mail(request.form["user"],
              "PROGESCO Teams: Confirmer l'inscription",
              "Ouvrez le lien suivant pour confirmer votre inscription : {redirect}",
              "Pour finaliser la création de votre compte sur PROGESCO Teams, cliquez sur le boutton 'Confirmer l'inscription' ou ouvrez le lien suivant : @link.",
              request.url_root + "account/signup/" + random_uuid,
              "Confirmer l'inscription")
    return render_template("signup.html", mail_address=request.form["user"])


@app.route("/account/reset", methods=["GET", "POST"])
def reset():
    if request.method == "POST":
        if request.form["user"] not in users:
            return render_template("reset.html", error=f"Le compte {request.form['user']} n'existe pas.")
        random_uuid: str = str(uuid.uuid4())
        password_resets[random_uuid] = request.form["user"]
        send_mail(request.form["user"],
                  "PROGESCO Teams: Réinitialiser le mot de passe",
                  "Ouvrez le lien suivant pour réinitialiser votre mot de passe : {redirect}",
                  "Pour réinitialiser votre mot de passe, cliquez sur le boutton \"Réinitialiser le mot de passe\" ou ouvrez le lien suivant : @link.",
                  request.url_root + "account/reset/" + random_uuid,
                  "Réinitialiser le mot de passe"
        )
        return render_template("signup.html", mail_address=request.form["user"])
    return render_template("reset.html")


@app.route("/account/reset/<uuid:id_reset>", methods=["GET", "POST"])
def reset_password(id_reset):
    """
    Reset account, link from mail.

    Page '/account/reset/<uuid:id_reset>'.
    """
    id_reset: str = str(id_reset)
    if request.method == "POST":
        print(password_resets)
        if id_reset not in password_resets:
            return abort(404)
        mail: str = password_resets[id_reset]
        if mail not in users:
            return render_template("login.html", error=f"Le compte {mail} n'existe pas.")
        users[mail] = hashlib.sha256(request.form["password"].encode()).hexdigest()
        with open("data/users.csv", "w") as file:
            writer: _csv.writer = csv.writer(file)
            writer.writerows(users.items())
        return redirect("/login?message=Nouveau mot de passe enregistré.")
    return render_template("reset_password.html")


@app.route("/manifest.json")
def manifest():
    """
    Manifest file.

    Redirects to static path.
    """
    return redirect("/static/manifest.json", 301)


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)

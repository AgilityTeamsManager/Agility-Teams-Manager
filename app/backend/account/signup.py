#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agility Teams Manager - Backend: Account signup.

Backend function for signup.
"""
import _csv, csv
import hashlib
import uuid

from flask import redirect, render_template

from app.backend.utils import send_mail
import app.modules.common as common  # Global data
from app.modules.data import save_users_data

signups: dict[str, dict[str, str]] = {}


@app.route("/account/signup/<uuid:id_confirm>")
def signup_confirm(id_confirm):
    """
    Confirm signup.
    """
    entry: dict[str, str] = signups[str(id_confirm)]
    print(entry)
    if entry["user"] in common.users:
        return render_template("login.html", error=f"Le compte {entry['user']} existe dèjà.")
    # Add to CSV file
    with open("data/users.csv", "a") as file:
        writer: _csv.writer = csv.writer(file)
        hashed: str = entry["password"]
        writer.writerow([entry["user"], hashed])
        users[entry["user"]] = hashed
    # Make data directory
    datadir: str = "data/" + entry["user"] + "/"
    try:
        os.mkdir(datadir)
    except FileExistsError:
        pass
    pickle.dump({}, open(datadir + "competitions.dat", "wb"))
##    user_data[entry["user"]] = []
##    pickle.dump(user_data, open("data/data.dat", "wb"))
    return redirect("/login?message=Inscription réussie")


@app.route("/account/signup", methods=["POST"])
def signup():
    """
    Signup.

    Send an email.
    """
    if request.form["user"] in common.users:
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agility Teams Manager - Backend: Account reset.

Backend function to reset account password.
"""
import _csv, csv
import hashlib
import uuid

from flask import redirect, render_template, abort

from app.backend.utils import send_mail
import app.modules.common as common  # Global data
from app.modules.data import save_users_data


def reset():
    """
    Handlemain account reset page.

    Page /account/reset.
    """
    if request.method == "POST":
        if request.form["user"] not in common.users:
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


def reset_password(id_reset):
    """
    Reset account, link from mail.

    Page /account/reset/<uuid:id_reset>.
    """
    id_reset: str = str(id_reset)
    if request.method == "POST":
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

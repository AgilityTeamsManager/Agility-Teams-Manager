#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agility Teams Manager - Backend for signup.
Copyright (C) 2022  Virinas-code

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import uuid

from flask import redirect, render_template, request

from app.utils import send_mail
import app.common as common  # Global data

signups: dict[str, dict[str, str]] = {}


def signup_confirm(id_confirm: uuid.UUID):
    """
    Confirm signup.

    Page /account/singup/<uuid:id_confirm>.

    :param uuid.UUID id_confirm: Signup request ID.
    """
    entry: dict[str, str] = signups[str(id_confirm)]
    if entry["user"] in common.data.users:
        return render_template("login.html", error=f"Le compte {entry['user']} existe dèjà.")
    common.data.add_user(entry["user"], entry["password"])
    return redirect("/account/login?message=Inscription réussie")


def signup():
    """
    Signup. Send an email.

    Page /account/signup, methods POST.
    """
    if request.form["user"] in common.data.users:
        return render_template("login.html", error=f"Le compte {request.form['user']} existe dèjà.")
    random_uuid: str = str(uuid.uuid4())
    signups[random_uuid] = {"user": request.form["user"],
                            "password": request.form["password"]}
    send_mail(request.form["user"],
              "PROGESCO Teams: Confirmer l'inscription",
              "Ouvrez le lien suivant pour confirmer votre inscription : {redirect}",
              "Pour finaliser la création de votre compte sur PROGESCO Teams, cliquez sur le boutton 'Confirmer l'inscription' ou ouvrez le lien suivant : @link.",
              request.url_root + "account/signup/" + random_uuid,
              "Confirmer l'inscription")
    return render_template("account/common/mail_received.html", mail_address=request.form["user"])

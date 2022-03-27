#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Backend function to reset account password."""
# Copyright (C) 2022  Virinas-code

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import uuid

from flask import abort, redirect, render_template, request

from app.utils import send_mail
import app.common as common  # Global data


password_resets: dict[str, str] = {}


def reset():
    """
    Handle main account reset page.

    Page /account/reset.
    """
    if request.method == "POST":
        if request.form["user"] not in common.data.users:
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
        return render_template("account/common/mail_received.html", mail_address=request.form["user"])
    return render_template("account/reset/reset.html")


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
        if mail not in common.users.users:
            return render_template("login.html", error=f"Le compte {mail} n'existe pas.")
        common.users.set_user_password(mail, request.form["password"])
        common.users.write_users_data()
        return redirect("/login?message=Nouveau mot de passe enregistré.")
    return render_template("account/reset/reset_password.html")

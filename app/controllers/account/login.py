#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Backend for login."""
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
from flask import redirect, render_template, request, session

from app.utils import hash_password, send_mail
import app.common as common  # Global data


def login():
    """
    Login page.

    Page /account/login, methods GET and POST.
    """
    if request.method == "POST":
        # Check password
        if request.form["user"] in common.data.users:
            if hash_password(request.form["password"]) == common.data.users[request.form["user"]].password:
                session["auth"] = request.form["user"]
                return redirect("/app")
            return render_template("account/root/login.html", error="Mauvais mot de passe")
        return render_template("account/root/login.html", error="Utilisateur inconnu")
    return render_template("account/root/login.html")

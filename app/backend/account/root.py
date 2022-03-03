#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agility Teams Manager - Backend: Account reset.

Backend function to reset account password.
"""
import _csv, csv

from flask import redirect, render_template

from app.backend.utils import send_mail
import app.modules.common as common  # Global data
from app.modules.data import save_users_data


def login():
    """
    Login page.

    Page /account/login, methods GET and POST.
    """
    if request.method == "POST":
        # Check password
        if request.form["user"] in common.users:
            if hashlib.sha256(request.form["password"].encode()).hexdigest() == common.users[request.form["user"]]:
                session["auth"] = request.form["user"]
                return redirect("/app")
            else:
                return render_template("login.html", error="Mauvais mot de passe")
        else:
            return render_template("login.html", error="Utilisateur inconnu")
    return render_template("login.html")

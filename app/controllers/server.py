#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agility Teams Manager.


Classements par équipe pour sportscanins.fr.
"""
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
import logging
from operator import methodcaller
import os
import sys

import coloredlogs
from flask import Flask

sys.path.append(os.path.abspath("."))

os.environ[
    "COLOREDLOGS_LOG_FORMAT"
] = "%(asctime)s [%(name)-25s] %(levelname)s %(message)s"
coloredlogs.install(level=15)
logging.basicConfig(
    format=os.environ["COLOREDLOGS_LOG_FORMAT"], level=logging.DEBUG
)

# Load env vars
from app.env import load_env_from_conf

load_env_from_conf()

from app.controllers.account.oauth import oauth
from app.controllers.account.delete import account_delete
from app.controllers.account.login import login
from app.controllers.account.logout import logout
from app.controllers.account.reset import reset, reset_password
from app.controllers.account.signup import signup, signup_confirm
from app.controllers.app.competition.root import app_competition
from app.controllers.app.competition.manage import app_competition_manage
from app.controllers.app.competition.load import app_competition_load
from app.controllers.app.root import (
    app_new,
    app_new_competition,
    app_root,
    app_settings,
)
from app.controllers.root import index
from app.controllers.session.session import (
    dev_session,
    session_join,
    session_new,
)
from app.controllers.static import public, static_ui
from app.data import DataManager

import app.common as common

common.init()

flask_app = Flask(__name__)
flask_app.secret_key = os.environ["ATM_APP_SECRET_KEY"]
flask_app.logger = logging.getLogger(__name__)
flask_app.template_folder = "../views/"
flask_app.static_folder = "../../data/"  # DEBUG TODO: Remove it

# Root URL
flask_app.add_url_rule("/", view_func=index)

# Static
flask_app.add_url_rule("/public/<path:filename>", view_func=public)
flask_app.add_url_rule("/ui/<path:filename>", view_func=static_ui)

# Account rules
# Delete
flask_app.add_url_rule("/account/delete", view_func=account_delete)

# Login
flask_app.add_url_rule(
    "/account/login", methods=["GET", "POST"], view_func=login
)

# Logout
flask_app.add_url_rule("/account/logout", view_func=logout)

# Signup
flask_app.add_url_rule("/account/signup", methods=["POST"], view_func=signup)
flask_app.add_url_rule(
    "/account/signup/<uuid:id_confirm>", view_func=signup_confirm
)

# Reset password
flask_app.add_url_rule(
    "/account/reset", view_func=reset, methods=["GET", "POST"]
)
flask_app.add_url_rule(
    "/account/reset/<uuid:id_reset>",
    view_func=reset_password,
    methods=["GET", "POST"],
)

# OAuth
flask_app.add_url_rule(
    "/account/auth", view_func=oauth, methods=["GET", "POST"]
)

# App
# Root
flask_app.add_url_rule("/app", view_func=app_root)
flask_app.add_url_rule("/app/settings", view_func=app_settings)
flask_app.add_url_rule("/app/new", view_func=app_new)
flask_app.add_url_rule(
    "/app/new/<int:id_competition>",
    view_func=app_new_competition,
    methods=["POST"],
)

# Competition
# Root
flask_app.add_url_rule("/app/<int:id_competition>", view_func=app_competition)

# Manage
flask_app.add_url_rule(
    "/app/<int:id_competition>/manage", view_func=app_competition_manage
)

# Load
flask_app.add_url_rule(
    "/app/<int:id_competition>/load", view_func=app_competition_load
)

# Session
# Dev session
flask_app.add_url_rule("/dev/session/", view_func=dev_session)
flask_app.add_url_rule("/dev/session/new", view_func=session_new)

# API
flask_app.add_url_rule(
    "/session/<uuid:session_id>/join/<string:team>", view_func=session_join
)


if __name__ == "__main__":
    os.environ["FLASK_ENV"] = "developpement"
    flask_app.run(host="localhost", port=8080, debug=True)

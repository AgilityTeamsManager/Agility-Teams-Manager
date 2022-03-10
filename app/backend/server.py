#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROGESCO Teams.

Classements par équipe pour PROGESCO.
"""
import logging
import os
import sys

from flask import Flask
import coloredlogs

sys.path.append(os.path.abspath("."))

# Load env vars
from app.env import load_env_from_conf
load_env_from_conf()

from app.backend.account.login import login
from app.backend.account.signup import signup, signup_confirm
##from app.backend.account.reset import reset, reset_password
from app.backend.root import index
from app.backend.static import public, static_ui
from app.data import DataManager

os.environ["COLOREDLOGS_LOG_FORMAT"] = "%(asctime)s: [%(module)-15s] %(message)s"
coloredlogs.install(level=logging.INFO)
logging.basicConfig(format=os.environ["COLOREDLOGS_LOG_FORMAT"], level=logging.DEBUG)

import app.common as common

flask_app = Flask(__name__)
flask_app.secret_key = os.environ["ATM_APP_SECRET_KEY"]
flask_app.logger = logging.getLogger(__name__)
flask_app.template_folder = "../frontend/"
flask_app.static_folder = "../../data/"  # DEBUG TODO: Remove it

common.data: DataManager = DataManager()

# Root URL
flask_app.add_url_rule("/", view_func=index)

# Static
flask_app.add_url_rule("/public/<path:filename>", view_func=public)
flask_app.add_url_rule("/ui/<path:filename>", view_func=static_ui)

# Account rules
# Login
flask_app.add_url_rule("/account/login", methods=["GET", "POST"],
                       view_func=login)

# Signup
flask_app.add_url_rule("/account/signup", methods=["POST"],
                       view_func=signup)
flask_app.add_url_rule("/account/signup/<uuid:id_confirm>",
                       view_func=signup_confirm)

# Reset password
##flask_app.add_url_rule("/account/reset", view_func=reset)
##flask_app.add_url_rule("/account/reset/<uuid:id_reset", view_func=reset_password)


if __name__ == "__main__":
    flask_app.run(host="localhost", port=8080, debug=True)

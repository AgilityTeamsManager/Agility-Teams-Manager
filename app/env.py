#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agility Teams Manager - Env load module.
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
import json
import os


def load_env_from_conf() -> None:
    """
    Load environnement variables from conf/ folder.

    :return: Nothing, sets environnement variables.
    """
    if "ATM_GMAIL_CLIENT_ID" not in os.environ or \
        "ATM_GMAIL_CLIENT_SECRET" not in os.environ or \
            "ATM_GMAIL_REFRESH_TOKEN" not in os.environ:
        # GMail variables not found!
        with open("conf/gmail.json") as gmail_conf:
            parsed: dict[str, str] = json.load(gmail_conf)
            os.environ["ATM_GMAIL_CLIENT_ID"] = parsed["client_id"]
            os.environ["ATM_GMAIL_CLIENT_SECRET"] = parsed["client_secret"]
            os.environ["ATM_GMAIL_REFRESH_TOKEN"] = parsed["refresh_token"]
    if "ATM_APP_SECRET_KEY" not in os.environ:
        with open("conf/app.json") as app_conf:
            parsed: dict[str, str] = json.load(app_conf)
            os.environ["ATM_APP_SECRET_KEY"] = parsed["secret_key"]

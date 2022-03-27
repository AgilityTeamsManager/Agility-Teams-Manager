#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Competitions list."""
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
from flask import render_template, session
from modules.models.user import User  # TODO: Debug

import app.common
from app.controllers.account.auth import check_auth


def app_root():
    """
    Shows competition list.

    Page /app.
    """
    return check_auth(
        render_template(
            "app/root/root.html",
            current_user=app.common.data.users[session.get("auth", None)],
        )
    )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Competition load page."""
# Agility Teams Manager - Teams ranking in agility competitions
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
from typing import Optional

from flask import render_template, session

import app.common
from app.controllers.account.auth import check_auth
from modules.data.models.user import DataUser


def app_competition_load(id_competition: int):
    """
    Main competition page.

    Page /app/<int:id_competition>/load.

    :param id_competition: Competition ID.
    :type id_competition: int
    """
    current_user: Optional[DataUser] = app.common.data.users[
        session.get("auth", None)
    ]
    return check_auth(
        render_template(
            "app/competition/load.html",
            competition=current_user.competitions[id_competition],  # type: ignore
        )
    )

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
import logging
from tabnanny import check
from typing import Optional
from django.shortcuts import render
from flask import (
    abort,
    flash,
    make_response,
    render_template,
    request,
    session,
)
from modules.data.models.user import DataUser
from modules.models.competition import Competition
from modules.models.user import User  # TODO: Debug

import app.common
from app.controllers.account.auth import check_auth
from modules.pyprogesco.scrapers.calendar import Calendar
from modules.utils import months

calendar: Calendar = Calendar()
agility_events: dict[int, list[Competition]] = calendar.list_events("Agility")
logger: logging.Logger = logging.getLogger("app.controllers.app.root")


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


def app_settings():
    """
    User settings.

    Page /app/settings.
    """
    return check_auth(
        render_template(
            "app/root/settings.html",
            current_user=app.common.data.users[session.get("auth", None)],
        )
    )


def app_new():
    """
    New competition page.

    Page /app/new.
    """
    return check_auth(
        render_template(
            "app/root/new.html", competitions=agility_events, months=months
        )
    )


def app_new_competition(id_competition: int):
    """
    Add a competition.

    Page /app/new/<int:id_competition>
    """
    logger.info(
        "User "
        + session["auth"]
        + " created new application "
        + request.form["name"]
        + " with image "
        + request.files["image"].filename
    )
    file_ext: str = request.files["image"].filename.split(".")[-1]
    if file_ext in ("png", "jpg", "jpeg"):
        # Do stuff
        current_user: Optional[DataUser] = app.common.data.users[
            session.get("auth", None)
        ]
        if current_user:
            # Find competition
            selected_competition: Optional[Competition] = None
            for month in range(1, 13):
                for competition in agility_events[month]:
                    if competition.id == id_competition:
                        selected_competition = competition
            if not selected_competition:
                logger.error("COMPETITION NOT FOUND: %s", id_competition)
                return abort(500)
            selected_competition.configure(request.form["name"], file_ext)
            current_user.add_competition(selected_competition)
        else:
            return abort(401)
    else:
        flash("Invalid file type", "error")
        logger.error("Invalid file type provided: %s", file_ext)
        return abort(
            make_response(
                check_auth(
                    render_template(
                        "app/root/new.html",
                        competitions=agility_events,
                        months=months,
                        message="Image non reconnue...",
                        preform_name=request.form["name"],
                    )
                )
            )
        )
    # print(request.form, request.files["image"])
    #  print(request.files["image"].stream.read())
    # print(file_ext)
    return abort(404)

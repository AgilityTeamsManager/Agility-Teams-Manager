#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Basic authentication sevice using session."""
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
from typing import Any
from flask import abort, session


def check_auth(data: Any) -> Any:
    """
    Checks if user is identified.

    Used in all app pages.

    :param Any data: Data returned when nothing happens.
    :return: 401 HTTP error if not authentified.
    """
    if session.get("auth", "") == "":
        return abort(401)
    else:
        return data

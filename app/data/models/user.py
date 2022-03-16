#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data module user model."""
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
import app.data.models as models


class User:
    """An user."""

    def __init__(self, mail_address: str, password: str) -> None:
        """
        Initialize new user.

        THIS DOESN'T RETRIEVE DATA.
        """
        self.mail: str = mail_address
        self.password: str = password
        self.competitions: dict[int, models.Competition] = {}
        """Competitions by ID."""

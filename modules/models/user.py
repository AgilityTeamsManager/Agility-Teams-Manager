#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""User model."""
# Agility Teams Manager - User model.
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
import pickle

from app.utils import hash_password
from modules.models.competition import Competition

logger: logging.Logger = logging.getLogger("modules.models.user")


class User:
    """An user."""

    def __init__(self, mail: str, password: str):
        """
        An user.

        :param str mail: Mail.
        :param str password: Hashed password.
        """
        logger.info("User %s: Creating with password %s", mail, password)
        self.mail: str = mail
        """Mail."""
        self.password: str = password
        """Password."""
        self.competitions: dict[int, Competition] = {}
        """Competitions."""

    def set_password(self, new_password: str) -> None:
        """
        Set password.

        :param new_password: New password, not hashed.
        :type new_password: str
        """
        self.password = hash_password(new_password)

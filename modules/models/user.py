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
from verboselogs import VERBOSE, VerboseLogger

from app.utils import hash_password
from modules.models.competition import Competition

logger: VerboseLogger = VerboseLogger("modules.models.user")


class User:
    """An user."""

    def __init__(self, mail: str, password: str):
        """
        An user.

        :param str mail: Mail.
        :param str password: Hashed password.
        """
        logger.log(
            VERBOSE, "User %s: Creating with password %s", mail, password
        )
        self.mail: str = mail
        """Mail."""
        self.password: str = password
        """Password."""
        self.competitions: dict[int, Competition] = {}
        """Competitions."""

    def set_password(self, new_password: str) -> None:
        """
        Set password.

        .. warning::
            This performs hash on password.

        :param new_password: New password, not hashed.
        :type new_password: str
        """
        self.password = hash_password(new_password)

    def add_competition(self, competition: Competition) -> None:
        """
        Add a configured competition to user.

        :param competition: Competition to add.
        :type competition: Competition
        """
        self.competitions[competition.id] = competition

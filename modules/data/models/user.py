#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extended user model with data functions."""
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
import logging
import pickle

from modules.models.competition import Competition
from modules.models.user import User

logger: logging.Logger = logging.getLogger("modules.data.models.user")


class DataUser(User):
    """User with data functions."""

    def load(self) -> None:
        """
        Loads data from data/ folder.

        Loads competitions of user.
        """
        logger.info("User %s: Loading data", self.mail)
        data_path: str = "data/" + self.mail + "/"
        with open(data_path + "competitions.dat", "br") as competitions_list:
            competitions: list[int] = pickle.load(competitions_list)
            for competition_id in competitions:
                competition: Competition = Competition.load(
                    self.mail, competition_id
                )
                self.competitions[competition_id] = competition

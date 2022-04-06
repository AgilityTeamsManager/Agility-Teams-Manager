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
import pickle

from verboselogs import VERBOSE, VerboseLogger

from modules.data.models.competition import DataCompetition
from modules.models.competition import Competition
from modules.models.user import User

logger: VerboseLogger = VerboseLogger("modules.data.models.user")


class DataUser(User):
    """User with data functions."""

    def load(self) -> None:
        """
        Load data from data/ folder.

        Load competitions of user.
        """
        logger.verbose("User %s: Loading data", self.mail)
        data_path: str = "data/" + self.mail + "/"
        with open(data_path + "competitions.dat", "br") as competitions_list:
            competitions: list[int] = pickle.load(competitions_list)
            for competition_id in competitions:
                competition: DataCompetition = DataCompetition.load(
                    self.mail, competition_id
                )
                self.competitions[competition_id] = competition

    def save(self):
        """
        Save user data to data/.

        Save user data.
        """
        logger.verbose("User %s: Saving data", self.mail)
        data_path: str = "data/" + self.mail + "/"
        with open(data_path + "competitions.dat", "bw") as competitions_list:
            competitions: list[int] = []
            for competition in self.competitions.values():
                competitions.append(competition.id)
                competition.save()
            pickle.dump(competitions, competitions_list)

    def add_competition(self, competition: Competition) -> None:
        super().add_competition(competition)
        self.save()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extended competition model with data functions."""
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
import os
import pickle

from verboselogs import VerboseLogger

from modules.models.competition import Competition
from modules.models.team import Team

logger: VerboseLogger = VerboseLogger("modules.data.models.competition")


class DataCompetition(Competition):
    """Competition with data functions."""

    def __init__(
        self, id: int, type: str, format: str, day: str, region: str, club: str
    ) -> None:
        super().__init__(id, type, format, day, region, club)
        self.teams: dict[str, Team] = {}
        """Map between team name and team."""
        self.name: str = ""
        """Competition name. Only available when configured."""
        self.image: str = ""
        """Competition image extension."""
        self.sessions: dict[str, DataSession] = {}
        """Competition concurrents' sessions."""
        self.concurrents: dict[int, Concurrent] = {}
        """Competition's concurrents."""

    @classmethod
    def load(cls, user: str, competition_id: int):
        """
        Load competition from user data.

        :param user: User's mail.
        :type user: str
        :param competition_id: Competition ID.
        :type competition_id: int
        :return: Competition loaded.
        :rtype: Competition
        """
        logger.verbose("User %s: Loading competition %s", user, competition_id)
        with open(
            "data/" + user + "/" + str(competition_id) + "/info.dat", "br"
        ) as file:
            data: dict[str, str] = pickle.load(file)
            instance = cls(
                int(data["id"]),
                data["type"],
                data["format"],
                data["day"],
                data["region"],
                data["club"],
            )
            instance.name = data["name"]
            instance.image = data["image"]
            return instance

    @classmethod
    def from_competition(cls, competition: Competition, name: str, image: str):
        """
        Make data competition from standard competition.

        :param competition: Base competition.
        :type competition: Competition
        """
        instance = cls(
            competition.id,
            competition.type,
            competition.format,
            competition.day,
            competition.region,
            competition.club,
        )
        instance.name = name
        instance.image = image
        return instance

    def to_dict(self) -> dict[str, str]:
        infos: dict[str, str] = super().to_dict()
        infos["name"] = self.name
        infos["image"] = self.image
        return infos

    def save(self, mail: str) -> None:
        """
        Save competition.

        :param str mail: Competition manager's mail.
        """
        logger.verbose("User %s: Saving competition %s", mail, self.id)
        base: str = "data/" + mail + "/" + str(self.id) + "/"
        if not os.path.exists(base):
            os.mkdir(base)
        # Save infos
        infos: dict[str, str] = self.to_dict()
        with open(base + "info.dat", "bw") as file:
            pickle.dump(infos, file)
        # Save sessions
        if not os.path.exists(base + "session"):
            os.mkdir(base + "session")

        for session_id, session in self.sessions.items():
            session.save(mail, self.id, session_id)

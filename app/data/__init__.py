#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agility Teams Manager - Data module.
Copyright (C) 2022  Virinas-code

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import hashlib
import logging
import pickle

import app.data.models as models


class DataManager:
    """
    The base data manager objects.

    Used to acces data in the data/ folder.
    """

    def __init__(self) -> None:
        """
        Initialize data manager.

        THIS WILL LOAD ALL DATA.
        Uses logging to log data load.
        """
        self.users_data: dict[str, str] = {}
        """Raw users data."""
        self.users: dict[str, models.User] = self.load_users()
        """Users."""

    def load_users(self) -> dict[str, models.User]:
        """
        Load users list.

        Get data from data/users.dat file and parse it.

        :return: List of users.
        :rtype: list[models.User]
        """
        logging.info("Loading data...")
        with open("data/users.dat", "br") as file:
            parsed: dict[str, str] = pickle.load(file)
            self.users_data = parsed
        users: dict[str, models.User] = []
        for mail, password in parsed.items():
            user: models.User = models.User(mail, password)
            path: str = "data/" + mail + "/competitions.dat"
            competitions: list[int] = pickle.load(open(path, "br"))
            for competition in competitions:
                user.competitions.append(self.load_competition(mail, competition))
            users[mail] = user
        self.users = users
        logging.info("Loaded data.")
        return users

    def load_competition(self, mail: str, id_competition: int) -> models.Competition:
        """
        Load a competition.

        This only loads data, and return the competition object with associated data.

        :param str mail: Competition's manager mail address.
        :param int id_competition: sportscanins competition's id.
        :return: Competition object.
        :rtype: models.Competition
        """
        logging.debug("Loading competition %(id_competition)s for user %(mail)s")
        competition: models.Competition = models.Competition(id_competition)
        path: str = "data/" + mail + "/" + str(id_competition) + "/info.dat"
        with open(path, "br") as file:
            data: dict[str, str] = pickle.load(file)
            competition.name = data["name"]
            competition.type = data["type"]
            competition.date = data["date"]
        return competition

    def add_user(self, mail: str, password: str) -> None:
        """
        Add a new user.

        /!\\ This function performs hash on password.

        :param str mail: User's mail address.
        :param str password: User's password.
        :return: Nothing.
        """
        logging.info("Creating user %(mail)s")
        hashed_password: str = hashlib.sha256(password.encode).hexdigest()
        user: models.User = models.User(mail, hashed_password)
        self.users.append(user)
        self.users_data[mail] = hashed_password
        self.write_users_data()

    def write_users_data(self) -> None:
        """
        Write users data to data/users.dat file.

        Takes data from users_data property.

        :return: Nothing.
        """
        logging.debug("Writting user data")
        with open("data/users.dat", "bw") as file:
            pickle.dump(self.users_data, file)

    def add_competition(self, mail: str, id_competition: int) -> None:
        """
        Add a new competition.
        """
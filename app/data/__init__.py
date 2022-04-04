#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data module."""
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
import hashlib
import logging
import os
import pickle
from typing import Optional

import app.data.models as models
from app.utils import hash_password
from modules.models.competition import Competition
from modules.data.models.user import DataUser


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
        self.users: dict[Optional[str], Optional[DataUser]] = self.load_users()
        """Users."""

    def load_users(self) -> dict[Optional[str], Optional[DataUser]]:
        """
        Load users list.

        Get data from data/users.dat file and parse it.

        :return: List of users.
        :rtype: list[DataUser]
        """
        logging.info("Loading users data...")
        with open("data/users.dat", "br") as file:
            parsed: dict[str, str] = pickle.load(file)
            self.users_data = parsed
        users: dict[Optional[str], Optional[DataUser]] = {}
        for mail, password in parsed.items():
            user: DataUser = DataUser(mail, password)
            user.load()
            users[mail] = user
        users[None] = None
        logging.info("Loaded users data.")
        return users

    def load_competition(self, mail: str, id_competition: int) -> Competition:
        """
        Load a competition.

        This only loads data, and return the competition object with associated data.

        :param str mail: Competition's manager mail address.
        :param int id_competition: sportscanins competition's id.
        :return: Competition object.
        :rtype: Competition
        """
        logging.debug(
            "Loading competition %(id_competition)s for user %(mail)s"
        )
        path: str = "data/" + mail + "/" + str(id_competition) + "/info.dat"
        with open(path, "br") as file:
            data: dict[str, str] = pickle.load(file)
            compet_name: str = data["name"]
            compet_image: str = data["image"]
            compet_id: int = data["id"]
            compet_type: str = data["type"]
            compet_format: str = data["format"]
            compet_day: str = data["day"]
            compet_club: str = data["club"]
        competition: Competition = Competition(
            compet_id, compet_type, compet_format, compet_day, compet_club
        )
        competition.configure(compet_name, compet_image)
        return competition

    def add_user(self, mail: str, password: str) -> None:
        """
        Add a new user.

        /!\\ This function performs hash on password.

        :param str mail: User's mail address.
        :param str password: User's password.
        :return: Nothing.
        """
        logging.info("Creating user %(mail)s" % {"mail": mail})
        hashed_password: str = hashlib.sha256(password.encode()).hexdigest()
        user: models.DataUser = models.DataUser(mail, hashed_password)
        path: str = "data/" + mail + "/"
        print(os.getcwd())
        os.mkdir(path)
        pickle.dump({}, open(path + "competitions.dat", "bw"))
        self.users[mail] = user
        self.users_data[mail] = hashed_password
        self.write_users_data()

    def set_user_password(self, mail: str, password: str) -> None:
        """
        Change an user password.

        /!\\ This function performs hash on password.

        :param str mail: User to change password.
        :param str password: New password.
        :return: Nothing, updates data.
        """
        new_password: str = hash_password(password)
        self.users[mail].password = new_password
        self.users_data[mail] = new_password

    def write_users_data(self) -> None:
        """
        Write users data to data/users.dat file.

        Takes data from users_data property.

        :return: Nothing.
        """
        logging.debug("Writting user data")
        with open("data/users.dat", "bw") as file:
            pickle.dump(self.users_data, file)

    def add_competition(
        self, mail: str, id_competition: int, competition: Competition
    ) -> None:
        """
        Add a new competition.

        :param str mail: Competition manager's mail.
        :param int id_competition: Competition ID on sportscanins.
        :return: Nothing. Use user.competitions[].
        """
        # We must have an unified model
        self.users[mail].competitions[id_competition] = competition

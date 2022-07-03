#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pysportscanins - Session.

Login to sportscanins.fr account.
"""
# Agility Teams Manager - Team ranking for agility competitions
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

from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.remote.webelement import WebElement


class Session:
    """An user session."""

    def __init__(self, username: str, password: str):
        """
        Create and login to a new session.

        :param username: Username (mail address).
        :type username: str
        :param password: Password.
        :type password: str
        """
        driver_options: FirefoxOptions = FirefoxOptions()
        driver_options.binary_location = os.path.abspath(
            "./lib/firefox/firefox"
        )
        # driver_options.headless = True
        os.environ["PATH"] += ":" + os.path.abspath(
            "./lib/"
        )  # Add driver to PATH
        self.driver = Firefox(options=driver_options)
        self.login(username, password)

    def login(self, username: str, password: str) -> None:
        """
        Login to sportscanins.fr account.

        :param username: Username.
        :type username: str
        :param password: Password.
        :type password: str
        """
        self.driver.get(
            "https://sportscanins.fr/calendrier/mon_espace_cneac.php"
        )
        username_input: WebElement = self.driver.find_element_by_id(
            "identifiant"
        )
        username_input.send_keys(username)
        password_input: WebElement = self.driver.find_element_by_id("pass")
        password_input.send_keys(password)
        login_button: WebElement = self.driver.find_element_by_id(
            "btnMotDePasse"
        )
        login_button.click()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agility Teams Manager - Data module competition model.
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


class Competition:
    """A competition."""

    def __init__(self, mail: str, id_competition: int) -> None:
        """
        Initialize new competition.

        THIS DOESN'T RETRIEVE DATA.

        :param str mail: Owner's mail address. Used for data management.
        :param int id_competition: sportscanins competition's id.
        :return: Nothing, access properties to get data.
        """
        self.id_competition: int = id_competition
        """Competition sportscanins.fr ID."""
        self.image: str = "data/" + mail + "/" + str(self.id_competition) + "/image.jpeg"
        """Path to competition logo."""
        self.name: str = ""
        """Competition's name."""
        self.date: str = ""
        """Day of competition, in French."""
        self.type: str = ""
        """Competition's type."""

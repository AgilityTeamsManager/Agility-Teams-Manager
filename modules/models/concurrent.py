#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Concurrent model."""
# Agility Teams Manager - Concurrent model.
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


class Concurrent:
    """A concurent."""

    def __init__(self, name: str, club: str, tels: str, mail: str):
        """
        A concurrent.

        :param str name: Name.
        :param str club: Club.
        :param str tels: Telephone numbers.
        :param str mail: Mail address.
        """
        self.name: str = name
        """Name."""
        self.club: str = club
        """Club."""
        self.tels: str = tels
        """Telephone numbers."""
        self.mail: str = mail
        """Mail address."""
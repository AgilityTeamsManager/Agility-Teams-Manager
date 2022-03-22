#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dog model."""
# Agility Teams Manager - Dog model.
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


class Dog:
    def __init__(self, name: str, category: str, grade: int):
        """
        A dog.

        :param str name: Name.
        :param str category: Category (A-D).
        :param int grade: Grade (1-3).
        """
        self.name: str = name
        """Name."""
        self.category: str = category
        """Category."""
        self.grade: int = grade
        """Grade."""

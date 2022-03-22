#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Group model.

.. note::
    A group is a concurrent + a dog.

    The unique key of a group is the record ID.
"""
# Agility Teams Manager - Group model.
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
from modules.models.concurrent import Concurrent
from modules.models.dog import Dog


class Group:
    def __init__(self, concurrent: Concurrent, dog: Dog) -> None:
        """
        Create a new group.

        :param modules.models.concurrent.Concurrent concurrent: Concurrent.
        :param modules.models.dog.Dog dog: Dog.
        """
        self.concurrent: Concurrent = concurrent
        """Concurrent."""
        self.dog: Dog = dog
        """Dog."""

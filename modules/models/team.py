#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Team model.

.. note::
    A team is a list of groups.
"""
# Agility Teams Manager - Team model.
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
from modules.models.group import Group


class Team:
    """A team."""

    def __init__(self, name: str, grade: int, category: str,
                 leader: Group, *args: Group) -> None:
        """
        Create a new team.

        :param str name: Team name.
        :param int grade: Team grade, None if no grades.
        :param str category: Team category, None if no category.
        :param Group leader: Team leader.
        :param modules.models.group.Group concurrent:
            Members of team.
        """
        self.name: str = name
        """Name of the team."""
        self.leader: Group = leader
        """Leader of team."""
        self.members: list[Group] = list(args)
        """Members."""
        self.members.append(self.leader)
        self.grade: int = grade
        """Team grade."""
        self.category: str = category
        """Team category."""

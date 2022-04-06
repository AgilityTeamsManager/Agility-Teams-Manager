#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agility Teams Manager - Unified competition model.
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
import logging
import os.path
import pickle

logger: logging.Logger = logging.getLogger("modules.models.competition")


class Competition:
    """The competition model."""

    def __init__(
        self, id: int, type: str, format: str, day: str, region: str, club: str
    ) -> None:
        """
        Create a new event.

        Used by pyprogesco and the data module.

        :param int id: sportscanins ID.
        :param str type: Competition type, like AGI or OBR.
        :param str format: Competition format, like "Concours standard".
        :param str day: Competition day.
        :param str region: Competition region.
        :param str club: Competition organization club.
        """
        self.id: int = id
        """sportscanins ID."""
        self.type: str = type
        """Competition type, like AGI or OBR."""
        self.format: str = format
        """Competition format, like "Concours standard"."""
        self.day: str = day
        """Competition day."""
        self.region: str = region
        """Club's region."""
        self.club: str = club
        """Competition orgnization club."""
        self.configured: bool = False
        """Wether the event is configured for the data module or not."""
        self.name: str = ""
        """Competition name. Only available when configured."""
        self.image: str = ""
        """Competition image extension."""

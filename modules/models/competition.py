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
from typing import Any, Union

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

    def to_dict(self) -> dict[str, str]:
        """
        Save object as dict.

        :return: A JSON compatible dict.
        :rtype: dict[str, Union[str, int, bool]]
        """
        return {
            "id": str(self.id),
            "type": self.type,
            "format": self.format,
            "day": self.day,
            "region": self.region,
            "club": self.club,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        """
        Load competition from dict.

        :param data: Data from :meth:`from_dict`.
        :type data: dict[str, Union[str, int, bool]]
        """
        return cls(
            int(data["id"]),
            data["type"],
            data["format"],
            data["day"],
            data["region"],
            data["club"],
        )

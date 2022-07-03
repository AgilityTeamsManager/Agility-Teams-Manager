#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pysportscanins - Organisator events.

Manage events.
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
import bs4
from selenium.webdriver import Firefox
import verboselogs

from modules.pyprogesco.session.orga_events.event import Event

logger: verboselogs.VerboseLogger = verboselogs.VerboseLogger(
    "modules.pyprogesco.session.orga_events"
)


class OrgaEvents:
    """Organisator events."""

    def __init__(self, driver: Firefox):
        """
        Load organisator events.

        :param driver: Driver logged in.
        :type driver: Firefox
        """
        logger.verbose("Loading events")
        self.driver: Firefox = driver
        """Logged in driver."""
        self.current_events, self.past_events = self.load_events()
        """Past events."""

    def load_events(self) -> tuple[dict[int, Event], dict[int, Event]]:
        """
        Load events list.

        :return: Events, sorted by ID.
        :rtype: dict[int, Event]
        """
        logger.verbose("Loading events list")
        self.driver.get(
            "https://sportscanins.fr/calendrier/mon_espace_cneac.php"
        )
        self.driver.find_element_by_id("tuile_7").click()
        source: str = self.driver.page_source
        parser: bs4.BeautifulSoup = bs4.BeautifulSoup(source)
        print(repr(parser))
        titles: bs4.ResultSet = parser.select("tr > td > h2")
        current_events_title: bs4.Tag = titles[0].parent.parent
        current_events: dict[int, bs4.Tag] = {}
        for tag in current_events_title.next_siblings:
            print("tag", repr(tag))
            if isinstance(tag, bs4.Tag):
                if tag.find_all("h2"):
                    break
                current_competition_id: int = int(
                    tag.find_all("td")[1]["onclick"]
                    .split("=")[2]
                    .split("&")[0]
                )
                current_events[current_competition_id] = tag
        # Load past events
        past_events_title: bs4.Tag = titles[2].parent.parent
        past_events: dict[int, bs4.Tag] = {}
        for tag in past_events_title.next_siblings:
            if isinstance(tag, bs4.Tag):
                if tag.find_all("h2"):
                    break
                past_competition_id: int = int(
                    tag.find_all("td")[1]["onclick"]
                    .split("=")[2]
                    .split("&")[0]
                )
                past_events[past_competition_id] = tag
        return current_events, past_events

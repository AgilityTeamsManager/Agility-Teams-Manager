#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pyprogesco Scrapers - Calendar.

Parse sportscanins.fr calendar data.
"""
import logging
from urllib.parse import urlparse, parse_qs, ParseResult

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from requests import get


class Event:
    """
    A sportscanins.fr public event.

    Use attributes to access data.
    """

    def __init__(self, **kwargs) -> None:
        """
        Initialize class.

        Use keyword arguments to set attributes.

        :return: Nothing.
        :rtype: None
        """
        self.__dict__ = kwargs


class Calendar:
    """
    The main class.

    Should be available as name "calendar" in main module.
    """

    def __init__(self) -> None:
        """
        Initialize calendar.

        Does all work to set variables.

        :return: Nothing.
        :rtype: None
        """
        """self.events: dict[str, dict[int, list[Event]]] = {"Toutes": self.list_events("Toutes"),
                                                          "Agility": self.list_events("Agility"),
                                                          "Flyball": self.list_events("Flyball"),
                                                          "Dog_Dancing": self.list_events("Dog_Dancing"),
                                                          "Hoopers": self.list_events("Hoopers"),
                                                          "Frisbee": self.list_events("Frisbee"),
                                                          "Canicross": self.list_events("Canicross"),
                                                          "Attelage": self.list_events("Attelage"),
                                                          "CAESC": self.list_events("CAESC"),
                                                          "Pass": self.list_events("Pass"),
                                                          "Formation": self.list_events("Formation")}"""
        self.events = {"Agility": self.list_events("Agility")}

    def list_events(self, activity: str = None, param_month: int = None) -> dict[int, list[Event]]:
        """
        Lists all incoming events in France.

        Does not filter region but filter months and activities.

        :return: List of events by month.
        :rtype: dict[int, list[Event]]
        """
        result: dict[int, list[Event]] = {}
        months: list[int] = [param_month]
        if not param_month:
            months = range(1, 13)
        for month in months:
            if param_month:
                logging.debug("Loading...")
            else:
                logging.debug(f"Loading... {month}/12")
            result[month] = []
            if activity:
                url: str = "https://sportscanins.fr/calendrier/calendrier.php?codeRegionale=%&Activite=" + activity + "&mois=" + str(month)
            else:
                url: str = "https://sportscanins.fr/calendrier/calendrier.php?codeRegionale=%&mois=" + str(month)
            content: str = get(url).text
            parser: BeautifulSoup = BeautifulSoup(content, features="lxml")
            if parser.find(role="alert"):
                logging.warning(f"No competitions (activity {activity}, month {month})")
                continue
            table: Tag = parser.find(id="tablecalendrier")  # Extract table
            table.find("tr").extract()  # Remove title line
            for row in table.find_all("tr"):
                event: Event = Event()
                cells: ResultSet = row.find_all("td")
                event.type = cells[1].find("div").text.lstrip("\n").strip()
                main_cell: ResultSet = cells[2].contents
                event.format = main_cell[2].strip(" -\n")
                event.day = main_cell[1].text
                event.region = main_cell[4].lstrip("\n-").strip()
                event.club = " ".join(main_cell[5].text.lstrip("\n ").replace("\n", "").split())
                link: ParseResult = urlparse(main_cell[5]["href"])
                event.id = int(parse_qs(link.query)["IdConcours"][0])
                result[month].append(event)
        logging.debug("Loading... Done.")
        return result

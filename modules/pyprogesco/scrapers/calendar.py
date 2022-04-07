#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pyprogesco Scrapers - Calendar.

Parse sportscanins.fr calendar data.
"""
from datetime import date, timedelta
import json
import time
from typing import Union
from urllib.parse import urlparse, parse_qs, ParseResult

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from requests import get
from verboselogs import VerboseLogger

from modules.models.competition import Competition


logger: VerboseLogger = VerboseLogger("modules.pyprogesco.scrapers.calendar")


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
        #  self.events = {"Agility": self.list_events("Agility")}
        self.events: dict[str, dict[int, list[Competition]]] = {}

    @classmethod
    def from_cache(cls, activities: Union[tuple[str], str]):
        """
        Load calendar from cache.

        If there is no cache or cache is outdated, it generates a new one.

        :return: New calendar, loaded from cache.
        :rtype: Calendar
        """
        if isinstance(activities, str):
            activities = (activities,)  # type: ignore
        now: date = date.today()
        with open("conf/cache.json") as cache_conf:
            data: dict[str, dict[str, str]] = json.load(cache_conf)
        instance: Calendar = cls()
        for activity in activities:
            cache_date: date = date.fromisoformat(
                data["competitions"][activity]
            )
            if now - timedelta(3) < cache_date:
                # OK, on charge
                logger.verbose("Activity %s: Loading from cache", activity)
                with open("cache/competitions/" + activity + ".json") as file:
                    from_cache: dict[
                        str, list[dict[str, Union[str, int, bool]]]
                    ] = json.load(file)
                instance.events[activity] = {}
                for month in range(1, 13):
                    instance.events[activity][month] = []
                    for cached_competition in from_cache[str(month)]:
                        instance.events[activity][month].append(
                            Competition.from_dict(cached_competition)
                        )
            else:
                # Cache périmé...
                # On va load du coup
                logger.warning(
                    "Activity %s: Cache outdated, reloading",
                    activity,
                )
                json_data: dict[
                    str, list[dict[str, Union[str, int, bool]]]
                ] = {}
                events: dict[int, list[Competition]] = instance.list_events(
                    activity
                )
                instance.events[activity] = events
                for month in range(1, 13):
                    json_data[str(month)] = []
                    for competition in events[month]:
                        json_data[str(month)].append(competition.to_dict())
                with open(
                    "cache/competitions/" + activity + ".json", "w"
                ) as json_file:
                    json.dump(json_data, json_file)
                data["competitions"]["Agility"] = date.today().isoformat()
        with open("conf/cache.json", "w") as cache_conf_write:
            json.dump(data, cache_conf_write)
        return instance

    def list_events(
        self, activity: str, param_month: int = None
    ) -> dict[int, list[Competition]]:
        """
        Lists all incoming events in France.

        Does not filter region but filter months and activities.

        :return: List of events by month.
        :rtype: dict[int, list[Event]]
        """
        result: dict[int, list[Competition]] = {}
        months: list[int] = [param_month]
        if not param_month:
            months = range(1, 13)
        for month in months:
            if param_month:
                logger.verbose("Calendar: Loading...")
            else:
                logger.verbose("Calendar: Loading... %s/12", month)
            result[month] = []
            if activity:
                url: str = (
                    "https://sportscanins.fr/calendrier/calendrier.php?codeRegionale=%&Activite="
                    + activity
                    + "&mois="
                    + str(month)
                )
            else:
                url: str = (
                    "https://sportscanins.fr/calendrier/calendrier.php?codeRegionale=%&mois="
                    + str(month)
                )
            while True:
                try:
                    content: str = get(url).text
                    break
                except ConnectionError:
                    logger.warning("Calendar: Connection reseted")
                    time.sleep(10)
            parser: BeautifulSoup = BeautifulSoup(content, features="lxml")
            if parser.find(role="alert"):
                logger.warning(
                    "Calendar: No competitions (activity %s, month %s)",
                    activity,
                    month,
                )
                continue
            table: Tag = parser.find(id="tablecalendrier")  # Extract table
            table.find("tr").extract()  # Remove title line
            for row in table.find_all("tr"):
                cells: ResultSet = row.find_all("td")
                event_type = cells[1].find("div").text.lstrip("\n").strip()
                main_cell: ResultSet = cells[2].contents
                event_format = main_cell[2].strip(" -\n")
                event_day = main_cell[1].text
                event_region = main_cell[4].lstrip("\n-").strip()
                event_club = " ".join(
                    main_cell[5].text.lstrip("\n ").replace("\n", "").split()
                )
                link: ParseResult = urlparse(main_cell[5]["href"])
                event_id: int = int(parse_qs(link.query)["IdConcours"][0])
                competition: Competition = Competition(
                    event_id,
                    event_type,
                    event_format,
                    event_day,
                    event_region,
                    event_club,
                )
                result[month].append(competition)
        logger.verbose("Calendar: Done.")
        return result

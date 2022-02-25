#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pyprogesco Scrapers - Calendar.

Parse sportscanins.fr calendar data.
"""
import logging

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from requests import get

from modules.pyprogesco.objects import Concurrent



class OrgaEvent:
    """
    sportscanins.fr organisator events.

    Data for event, from ID.
    """

    def __init__(self, id_competition: int) -> None:
        """
        Initialize event.

        Use competition ID.

        :param int id_competition: Competition ID.
        :return: Nothing, use methods to get data.
        """
        self.id_competition: int = id_competition

    def concurrent_list(self, data: BeautifulSoup = None) -> list[Concurrent]:
        """
        Get principal concurrents list of event.

        Automatically fetch data if data param is absent.

        :param BeautifulSoup data: Data parser. Default is fetch from sportscanins.
        :return: List of concurrents.
        :rtype: list[modules.pyprogesco.objects.Concurrent]
        """
        table: Tag = data.find(class_="Tableau")
        table.find("tr").extract()  # Remove title line
        rows: ResultSet = table.find_all("tr")
        result: list[Concurrent] = []
        for row in rows:
            concurrent: Concurrent = Concurrent(True)
            cells: ResultSet = row.find_all("td")
            name_cell: list[Tag] = cells[1].contents
            dog: list[str] = name_cell[0].lstrip("\n ").split("[")
            concurrent.dog = dog[0][:-1]
            concurrent.dog_fapac = dog[1][:-1]
            dog_infos: list[str] = name_cell[2].lstrip(" ]\t\n").split(" - ")
            concurrent.dog_category = dog_infos[0]
            concurrent.dog_race = dog_infos[1]
            record: list[str] = name_cell[4].split(" [")
            concurrent.record = record[0]
            concurrent.record_id = int(record[1][3:].replace("\t", "").replace("\n", "")[:-2])
            concurrent.message = cells[1].find("span")
            if concurrent.message:
                concurrent.message = concurrent.message.text
            conductor_cell: list[Tag] = cells[2].contents
            name: list[str] = conductor_cell[0].strip(" ]\t\n").split(" [")
            concurrent.name = name[0]
            concurrent.license = name[1].strip("\t\n")
            concurrent.club = conductor_cell[2].strip("\t\n")
            concurrent.tels: list[str] = conductor_cell[4].strip("\t\n").split(" - ")
            concurrent.mail: str = conductor_cell[7].text
            epreuves: list[Tag] = cells[3]
            epreuves_list = []
            for tag in epreuves.contents:
                if type(tag) != Tag:
                    epreuves_list.append(tag)
            epreuves_list.pop()  # Remove trailing whitespace
            payement = cells[4].find("form").find("span").find("span")["class"][0]
            if payement == "iconev":
                concurrent.payement = "yes"
            elif payement == "iconeo":
                concurrent.payement = "waiting"
            elif payement == "iconer":
                concurrent.payement = "no"
            else:
                print(payement)
                concurrent.payement = "unknown"
            print(repr(concurrent.payement))
            result.append(concurrent)
        return result


"""class Event:
    ""
    A sportscanins.fr public event.

    Use attributes to access data.
    ""

    def __init__(self, **kwargs) -> None:
        ""
        Initialize class.

        Use keyword arguments to set attributes.

        :return: Nothing.
        :rtype: None
        ""
        self.__dict__ = kwargs


class Calendar:
    ""
    The main class.

    Should be available as name "calendar" in main module.
    ""

    def __init__(self) -> None:
        ""
        Initialize calendar.

        Does all work to set variables.

        :return: Nothing.
        :rtype: None
        ""
        self.events: dict[str, dict[int, list[Event]]] = {"Toutes": self.list_events("Toutes"),
                                                          "Agility": self.list_events("Agility"),
                                                          "Flyball": self.list_events("Flyball"),
                                                          "Dog_Dancing": self.list_events("Dog_Dancing"),
                                                          "Hoopers": self.list_events("Hoopers"),
                                                          "Frisbee": self.list_events("Frisbee"),
                                                          "Canicross": self.list_events("Canicross"),
                                                          "Attelage": self.list_events("Attelage"),
                                                          "CAESC": self.list_events("CAESC"),
                                                          "Pass": self.list_events("Pass"),
                                                          "Formation": self.list_events("Formation")}

    def list_events(self, activity: str = None, param_month: int = None) -> dict[int, list[Event]]:
        ""
        Lists all incoming events in France.

        Does not filter region but filter months and activities.

        :return: List of events by month.
        :rtype: dict[int, list[Event]]
        ""
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
                event.type = cells[1].find("div").lstrip("\n").strip()
                main_cell: ResultSet = cells[2].contents
                event.format = main_cell[2].strip(" -\n")
                event.day = main_cell[1].text
                event.region = main_cell[4].text.lstrip("\n-").strip()
                event.club = " ".join(main_cell[5].text.lstrip("\n ").replace("\n", "").split()
                link: ParseResult = urlparse(main_cell[5]["href"])
                event.id = parse_qs(link.query)["IdConcours"][0]
                result[month].append(event)
		logging.debug("Loading... Done.")
        return result"""

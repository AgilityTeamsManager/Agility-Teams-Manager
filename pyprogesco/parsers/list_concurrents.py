#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pyprogesco parser for concurrents list.

Parse data from sportscanins.fr.
"""
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet
import requests


class ListConcurrentsParser:
    """
    Parse concurrents list.

    Uses competition ID.
    """

    def __init__(self, id_competition: int) -> None:
        """
        Initialize system.

        :param int id_competition: The sportscanins.fr competition ID.
        :return: Nothing.
        :rtype: None
        """
        self.id_competition: int = id_competition

    def request(self) -> BeautifulSoup:
        """
        Get the parser of the contentent of the concurrents list.

        :return: The BeautifulSoup parser for the web page.
        :rtype: BeautifulSoup
        """
        url: str = "https://sportscanins.fr/calendrier/engagements_concurrent_liste.php"
        payload: dict[str, str] = {"IdConcours": self.id_competition}
        request: requests.Response = requests.post(url, data=payload)
        parser: BeautifulSoup = BeautifulSoup(request.text, features="lxml")
        return parser

    def parse(self, parser: BeautifulSoup) -> list[tuple[str, str, str]]:
        """
        Parse the web page from BeautifulSoup.

        :param BeautifulSoup parser: The BeautifulSoup parser of the web page.
        :return: List of concurrents (conductor + dog + category)
        :rtype: list[tuple[str, str]]
        """
        array: Tag = parser.find_all("table", class_="Tableau")[0]
        # Remove the introduction lines
        array.find("tr", class_="Ligne_de_titre").extract()
        array.find(text="Concurrents engagés à jour de paiement").parent.parent.parent.extract()
        # Find the "Liste d'attente" row
        waiting_list: Tag = array.find(text="Liste d'attente").parent.parent.parent
        # Remove elements after
        for tag in waiting_list.find_all_next():
            tag.extract()
        # Remove "Liste d'attente"
        waiting_list.extract()
        # Empty result list
        result: list[tuple[str, str, str]] = []
        # Fill the result list
        for row in array.find_all("tr"):
            cells: ResultSet = row.find_all("td")
            category: str = cells[2].text
            concurrent: str = cells[4].text.lstrip("\n\r\t").strip()
            dog: str = cells[1].text
            result.append((concurrent, dog, category))
        return result

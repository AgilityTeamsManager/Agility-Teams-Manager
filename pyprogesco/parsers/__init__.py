#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pyprogesco parsers.

Parse files and web pages.
"""
from urllib.parse import parse_qs, ParseResult, urlparse
from pyprogesco.parsers.list_concurrents import ListConcurrentsParser


class HTMLParser:
    """
    Parse HTML data from the competition page.

    Init with the base URL to competition page.
    """

    def __init__(self, page: str) -> None:
        """
        Init with base page and register parsers.

        :param str page: URL to competition page on sportscanins.fr.
        :return: Nothing.
        :rtype: None
        """
        self.url: str = page
        """Base URL to competition page."""
        self.id_competition: int = self.parse_id()
        """ID of the competition. Parsed by :pyobject: HTMLParser.parse_id"""
        self.concurrents_list: list[str] = ListConcurrentsParser(self.id_competition).get()

    def parse_id(self) -> int:
        """
        Parse the competition ID from the basse url.

        :return: Compettion id on sportscanins.fr.
        :rtype: int
        """
        parser: ParseResult = urlparse(self.url)
        query_parser: dict[str, list[str]] = parse_qs(parser.query)
        return int(query_parser["IdConcours"][0])

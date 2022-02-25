#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Concurrent object - Represents a competition concurrent.

From concurrent lists.
"""


class Concurrent:
    """
    A competition concurrent.

    For concurrent lists.
    """

    def __init__(self, orga: bool, **kwargs) -> None:
        """
        Initialize object.

        Write to keyword arguments to __dict__.

        :param bool orga: Organisator format.
        :return: Nothing.
        """
        self.orga: bool = orga
        self.__dict__ = kwargs

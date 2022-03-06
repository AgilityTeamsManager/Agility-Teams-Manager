#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agility Teams Manager - Backend static functions.
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
from flask import send_from_directory


def public(filename: str):
    """
    Provides static files for public/ directory.

    Page /public/<path:filename>.

    :param str filename: File to get.
    """
    return send_from_directory("../../public/", filename)


def static_ui(filename: str):
    """
    Provides static files for ui/ directory.

    Page /ui/<path:filename>.

    :param str filename: File to get.
    """
    return send_from_directory("../../ui/", filename)

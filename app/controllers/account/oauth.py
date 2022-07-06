#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Account - OAuth module.

Login to sportscanins.fr account.
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
from flask import render_template, request


def oauth():
    """
    Login to sportscanins.fr.

    Page /account/auth, methods GET and POST.
    """
    if request.method == "POST":
        
    return render_template("account/auth/sportscanins.html")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session backend.

Pages:
    - /session/<uuid:id_session>/

.. note::
    Also include a dev page (/dev/session)
"""
from flask import render_template

from modules.models.concurrent import Concurrent
from modules.models.dog import Dog
from modules.models.group import Group
from modules.models.team import Team


def dev_session():
    """
    A developpement test session.

    Page /dev/session.
    """
    current_concurrent: Concurrent = Concurrent("Test USER", "", "", "test.user@example.com")
    current_dog: Dog = Dog("Foo", "A", 1)
    other_dog: Dog = Dog("Bar", "A", 1)
    current_group: Group = Group(current_concurrent, current_dog)
    other_group: Group = Group(current_concurrent, other_dog)
    teams: list[Team] = [Team("Test team", 1, "A", current_group, other_group), Team("Another test team", 1, "C", current_group, current_group), Team("VIP team", 3, "A", current_group)]
    return render_template("/session/session.html", group=current_group,
                           teams=teams)

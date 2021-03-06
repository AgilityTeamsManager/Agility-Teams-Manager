#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session backend.

Pages:
    - /session/<uuid:id_session>/

.. note::
    Also include a dev page (/dev/session)
"""
from uuid import UUID, uuid4

from flask import abort, render_template, request

from modules.models.concurrent import Concurrent
from modules.models.dog import Dog
from modules.models.group import Group
from modules.models.team import Team


def dev_session():
    """
    A developpement test session.

    Page /dev/session.
    """
    current_concurrent: Concurrent = Concurrent(
        "Test USER", "", "", "test.user@example.com"
    )
    current_dog: Dog = Dog("Foo", "A", 1)
    other_dog: Dog = Dog("Bar", "A", 1)
    current_group: Group = Group(current_concurrent, current_dog)
    other_group: Group = Group(current_concurrent, other_dog)
    teams: list[Team] = [
        Team("Test team", 1, "A", current_group, other_group),
        Team("Another test team", 1, "C", current_group, current_group),
        Team("VIP team", 3, "A", current_group),
    ]
    return render_template(
        "/session/session.html",
        group=current_group,
        teams=teams,
        session_id=uuid4(),
    )


def session_join(session_id: UUID, team: str):
    """
    Join a team.

    Page /session/<uuid:id_session>/join/<string:team>.
    """
    print(session_id, team)
    return "OK"


def session_new():
    """
    Make a new team.

    Page /session/<uuid:id_session>/new.
    """
    if request.method == "POST":
        return abort(501)
    current_concurrent: Concurrent = Concurrent(
        "Test USER", "", "", "test.user@example.com"
    )
    current_dog: Dog = Dog("Foo", "A", 1)
    current_group: Group = Group(current_concurrent, current_dog)
    return render_template("/session/new.html", group=current_group)

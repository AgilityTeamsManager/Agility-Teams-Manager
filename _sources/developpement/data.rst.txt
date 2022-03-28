**********
Data model
**********

All the data is stored in the ``data/`` path.

Structure
=========

``users.dat``
    Users and passwords

    **Format:** Pickle (``dict[str, str]``)

``<user>/``
    User data

User data
---------

``competitions.dat``
    User competitions list.

    **Format:** Pickle (``list[int]``)

``<competition_id>/``
    Competition data.

Competition data
^^^^^^^^^^^^^^^^

``info.dat``
    Informations about competition.

    **Format:** Pickle (``dict[str, str]``)

    id
        Competition ID.

    type
        Competition type, like ``AGI``.

    format
        Competition format, like ``Concours Standard``.

    day
        Competition day.

    club
        Competition organization club.

    name
        Competition name.

    image
        Wether if the competition has an image or not.

    .. code-block:: json

        {
            "id": 1234,
            "type": "AGI",
            "format": "Concours Standard",
            "day": "Vendredi 13",
            "club": "GESC",
            "name": "Concours du Samedi",
            "image": true
        }

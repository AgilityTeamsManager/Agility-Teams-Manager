#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agility Teams Manager - Utils module.
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
import email.mime.multipart
import email.mime.text
import hashlib
import logging

from app.mail.gmail import send_mail as gmail_send_mail


def send_mail(
    to: str,
    subject: str,
    message: str,
    mail_message: str,
    redirect: str,
    button: str,
) -> None:
    """
    Send a Agility Teams Manager mail.

    :param str to: Destination address.
    :param str subject: Mail subject.
    :param str message: Text message.
    :param str mail_message: Message for HTML part.
    :param str redirect: Redirect link in mail.
    :param str button: Button's text.
    :return: Nothing.
    :rtype: None
    """
    logging.debug("Sending email to %(to)s")
    mail: email.mime.multipart.MIMEMultipart = (
        email.mime.multipart.MIMEMultipart("alternative")
    )
    mail["Subject"] = subject
    mail["From"] = "Agility Teams Manager<progesco.teams@gmail.com>"
    mail["To"] = to
    mail.attach(
        email.mime.text.MIMEText(message.format(redirect=redirect), "plain")
    )
    with open("app/frontend/mail.html") as file_object:
        mail_html: str = (
            file_object.read()
            .replace("@message", mail_message)
            .replace("@link", redirect)
            .replace("@button", button)
        )
        mail.attach(email.mime.text.MIMEText(mail_html, "html"))
    gmail_send_mail("progesco.teams@gmail.com", to, mail)


def hash_password(password: str) -> str:
    """
    Return hexdigest of password hash.

    :param str password: Password to hash.
    :return: Hexdigest of password hash.
    :rtype: str
    """
    return hashlib.sha256(password.encode()).hexdigest()

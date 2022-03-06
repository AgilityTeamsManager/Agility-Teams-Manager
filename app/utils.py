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
import os
import smtplib

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

print(os.getcwd())


def env_to_conf() -> None:
    """
    Write secrets from environnement variables to conf/ path.

    :return: Nothing.
    """
    with open("conf/credentials.json") as file:
        file.write(os.environ["GOOGLE_CREDENTIALS"])
    with open("conf/token.json") as file:
        file.write(os.environ["GOOGLE_TOKEN"])



def main():
    """
    Shows basic usage of the Gmail API.

    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('conf/token.json'):
        try:
            creds = Credentials.from_authorized_user_file('conf/token.json', SCOPES)
        except ValueError:
            pass
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'conf/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('conf/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        logging.error('An error occurred: %(error)s' % {"error": error})


if __name__ == '__main__':
    main()


def send_mail(to: str, subject: str, message: str, mail_message: str,
              redirect: str, button: str) -> None:
    """
    Send a PROGESCO Teams mail.

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
    mail: email.mime.multipart.MIMEMultipart = email.mime.multipart.MIMEMultipart("alternative")
    mail["Subject"] = subject
    mail["From"] = "PROGESCO Teams<progesco.teams@gmail.com>"
    mail["To"] = to
    mail.attach(email.mime.text.MIMEText(message.format(redirect=redirect), "plain"))
    with open("mail.html") as file_object:
        mail_html: str = file_object.read().replace("@message", mail_message) \
                                           .replace("@link", redirect) \
                                           .replace("@button", button)
        mail.attach(email.mime.text.MIMEText(mail_html, "html"))
    smtp_server: smtplib.SMTP_SSL = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp_server.login("progesco.teams@gmail.com", os.environ["SECRET_GMAIL"])
    smtp_server.sendmail("progesco.teams@gmail.com", to, mail.as_string())
    smtp_server.close()


def hash_password(password: str) -> str:
    """
    Return hexdigest of password hash.

    :param str password: Password to hash.
    :return: Hexdigest of password hash.
    :rtype: str
    """
    return hashlib.sha256(password.encode()).hexdigest()

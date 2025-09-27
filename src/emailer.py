"""
emailer.py sends the HTML content via SMTP using a stored token.
"""

import yagmail

from src.config import RECIPIENTS, SENDER_EMAIL, SMTP_PORT, SMTP_SERVER
from src.helpers import Email


def send_email(contents: str) -> None:
    """
    Sends the formatted HTML contents to all emails in the recipient list in src/config.py
    :param contents: HTML string
    :return: None
    """
    email = Email(
        subject="morning headlines",
        body=contents,
        recipients=RECIPIENTS,
        server=SMTP_SERVER,
        port=SMTP_PORT,
    )

    yag = yagmail.SMTP(
        user=SENDER_EMAIL, oauth2_file="~/.yagmail/eliadnomt.json", smtp_ssl=True
    )  # triggers one-time browser login & token storage

    for recipient in email.recipients:
        yag.send(to=recipient, subject=email.subject, contents=email.body)

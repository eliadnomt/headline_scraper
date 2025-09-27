"""
emailer.py sends the HTML content via SMTP using a stored token.
"""

import logging
from pathlib import Path

import yagmail
from yagmail.error import (YagAddressError, YagConnectionClosed,
                           YagInvalidEmailAddress)

from secret_files.secret_config import RECIPIENTS, SENDER_EMAIL, TOKEN_PATH
from src.config import SMTP_PORT, SMTP_SERVER
from src.helpers import Email

logger = logging.getLogger(__name__)


def send_email(contents: str) -> None:
    """
    Sends the formatted HTML contents to all emails in the recipient list in src/secret_config.py
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

    # Ensure token file exists before connecting
    if not Path(TOKEN_PATH).exists():
        logger.error("OAuth token file not found at %s", TOKEN_PATH)
        raise FileNotFoundError(f"OAuth token file missing: {TOKEN_PATH}")

    try:
        yag = yagmail.SMTP(
            user=SENDER_EMAIL,
            oauth2_file=str(TOKEN_PATH),
            smtp_ssl=True,
        )
    except (OSError, YagConnectionClosed) as e:
        logger.error("Failed to initialize SMTP connection: %s", e)
        raise

    for recipient in email.recipients:
        try:
            yag.send(to=recipient, subject=email.subject, contents=email.body)
            logger.info("Email sent to %s", recipient)
        except (YagInvalidEmailAddress, YagAddressError) as e:
            logger.warning("Invalid email address %s: %s", recipient, e)
        except OSError as e:
            logger.error("Failed to send email to %s: %s", recipient, e)
            raise

import ssl

import certifi
import yagmail
from config import RECIPIENTS, SMTP_SERVER, SMTP_PORT, SENDER_EMAIL
from helpers import Email


def send_email(contents: str) -> None:
	email = setup_email(contents)

	yag = yagmail.SMTP(
		user=SENDER_EMAIL,
		oauth2_file="~/.yagmail/eliadnomt.json",
		smtp_ssl=True
	)  # triggers one-time browser login & token storage

	for recipient in email.recipients:
		yag.send(to=recipient,
				 subject=email.subject,
				 contents=email.body)

def setup_email(contents: str) -> Email:
	result = Email(
		subject = "headlines - sustainable fashion",
		body = contents,
		recipients = RECIPIENTS,
		server = SMTP_SERVER,
		port = SMTP_PORT
	)

	return result

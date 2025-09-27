"""
helpers.py contains all Dataclass objects used to facilitate data handling in headline_scraper.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Article:
	"""A class to store RSS data for a scraped article."""

	title: str
	link: str
	publish_time: str


@dataclass
class TopicList:
	"""A class to map a list of Article objects to a given topic keyword(s)."""

	title: str
	article_list: list


@dataclass
class Email:
	"""A class to store all required information to send an email via SMTP."""

	subject: str
	body: str
	recipients: List[str]
	server: str
	port: int

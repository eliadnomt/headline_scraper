"""
format.py contains all the functions related to HTML formatting of scraped content for emailing.
"""

import logging
from datetime import datetime
from typing import List

from src.helpers import TopicList

logger = logging.getLogger(__name__)


def to_html(feed: List[TopicList]) -> str:
	"""
	Writes the html for the email message body, including formatting each scraped article.
	:param feed: a list of TopicList objects (see src/helpers.py).
	:return: HTML string
	"""
	logger.info("Converting scraped data to HTML")

	html = ""
	date = (
		f"{weekday_as_word(datetime.today().weekday())} {datetime.today().day} "
		f"{month_as_word(datetime.today().month)} {datetime.today().year}"
	)
	html += f"<h1>{date}</h1>"

	for topic in feed:
		html += f"<h2>{topic.title}</h2>"
		if len(topic.article_list) == 0:
			html += f"No news on {topic.title} today."
		else:
			for article in topic.article_list:
				split_link = article.title.split(" - ")

				html += (f"<p>{split_link[-1]} - {article.publish_time}<br>"
						 f"<a href='{article.link}'>{split_link[0]}</a><br></p>")

	logger.info("Finished HTML conversion")
	return html


def month_as_word(month: int) -> str:
	"""
	Convert datetime month integer to month word.
	:param month: datetime month integer
	:return: corresponding month string
	"""
	# TODO: implement multiple languages via config
	int_to_word_dict = {
		1: "january",
		2: "february",
		3: "march",
		4: "april",
		5: "may",
		6: "june",
		7: "july",
		8: "august",
		9: "september",
		10: "october",
		11: "november",
		12: "december",
	}
	return int_to_word_dict[month]


def weekday_as_word(day: int) -> str:
	"""
	Convert datetime weekday integer to weekday word.
	:param day: datetime day integer
	:return: corresponding weekday word
	"""
	int_to_word_dict = {
		0: "monday",
		1: "tuesday",
		2: "wednesday",
		3: "thursday",
		4: "friday",
		5: "saturday",
		6: "sunday",
	}
	return int_to_word_dict[day]

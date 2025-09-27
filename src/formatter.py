from datetime import datetime
from typing import List

from helpers import TopicList


def to_html(feed: List[TopicList]) -> str:
	html = ""
	date = f"{weekday_as_word(datetime.today().weekday())} {datetime.today().day} {month_as_word(datetime.today().month)} {datetime.today().year}"
	html += f"<h1>{date}</h1>"

	for topic in feed:
		html += f"<h2>{topic.title}</h2>"
		for article in topic.article_list:
			html += f"<p><a href='{article.link}'>{article.title}</a><br></p>"
	return html

def month_as_word(month: int) -> str:
	#TODO: implement multiple languages via config
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
		12: "december"
	}
	return int_to_word_dict[month]

def weekday_as_word(day: int) -> str:
	int_to_word_dict = {
		0: "monday",
		1: "tuesday",
		2: "wednesday",
		3: "thursday",
		4: "friday",
		5: "saturday",
		6: "sunday"
	}
	return int_to_word_dict[day]

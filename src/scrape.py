"""
scrape.py contains all functions associated with the parsing and organising of the
scraped RSS entries corresponding to the topic list in src/config.py.
"""

from typing import List

import feedparser
import logging
logger = logging.getLogger(__name__)

from src.helpers import Article, TopicList


def get_articles_for_all(topics: List[str]) -> List[TopicList]:
	"""
	Runs the scraper function for all search topics listed in src/config.py.
	:param topics: a list of topics from src/config.py
	:return: a list of TopicList objects which map all individual scraped
						articles to the topic group.
	"""
	feed = list()

	for topic in topics:
		topic_articles = get_articles_for_specific(topic)
		feed.append(topic_articles)

	return feed


def get_articles_for_specific(topic: str) -> TopicList:
	"""
	Uses the feedparser library to scrape the RSS entries for Google
		searches using the topic keywords in src/config.py.
	:param topic: a string containing one or more topic keywords.
	:return: a TopicList object which maps a list of Article objects to the topic keyword(s).
	"""
	url = f"https://news.google.com/rss/search?q={topic.replace(' ', '+')}"
	feed = feedparser.parse(url)

	article_list = list()

	for rss_entry in feed.entries:
		article_data = Article(title=rss_entry.title, link=rss_entry.link)
		article_list.append(article_data)

	logger.info(f"Retrieved RSS data for {len(article_list)} articles for topic {topic.upper()}")
	result = TopicList(topic, article_list)

	return result

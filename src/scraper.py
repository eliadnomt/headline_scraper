from typing import List

import feedparser
from feedparser import FeedParserDict

from helpers import Article, TopicList

def get_articles_for_all(topics: List[str]) -> List[TopicList]:
	feed = list()

	for topic in topics:
		topic_articles = get_articles_for_specific(topic)
		feed.append(topic_articles)

	return feed

def get_articles_for_specific(topic: str) -> TopicList:
	url = f"https://news.google.com/rss/search?q={topic.replace(' ', '+')}"
	feed = feedparser.parse(url)

	article_list = list()

	for rss_entry in feed.entries:
		article_data = extract_data(rss_entry)
		article_list.append(article_data)

	result = TopicList(
		topic,
		article_list
	)

	return result


def extract_data(item: FeedParserDict) -> Article:
	result = Article(
		title=item.title,
		link=item.link,
		description=item.get("summary", "")
	)
	return result

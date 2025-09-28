"""
scrape.py contains all functions associated with the parsing and organising of the
scraped RSS entries corresponding to the topic list in src/secret_config.py.
"""

import json
import logging
from json import JSONDecodeError
from pathlib import Path
from typing import List
from datetime import datetime
import feedparser

from src.config import CACHE_FILE
from src.helpers import Article, TopicList, HeadlineCache

logger = logging.getLogger(__name__)


def get_articles_for_all(topics: List[str]) -> List[TopicList]:
	"""
	Scrape all topics and return TopicList objects with new,
	deduplicated articles sorted by recency.
	"""
	results: List[TopicList] = []
	for topic in topics:
		results.append(get_articles_for_specific(topic))
	return results


def get_articles_for_specific(topic: str) -> TopicList:
	"""
	Scrape a single topic, filter out cached titles,
	and return new articles sorted by publish time (newest first).
	"""
	url = f"https://news.google.com/rss/search?q={topic.replace(' ', '+')}"
	feed = feedparser.parse(url)

	new_articles: List[Article] = []

	for rss_entry in feed.entries:
		published_str = getattr(rss_entry, "published", "")
		published_dt = None
		if hasattr(rss_entry, "published_parsed") and rss_entry.published_parsed:
			try:
				published_dt = datetime(*rss_entry.published_parsed[:6])
			except (TypeError, ValueError):
				published_dt = None

		article = Article(
			title=rss_entry.title,
			link=rss_entry.link,
			publish_time=published_str,  # remain string for templates
		)

		if check_cache(article):
			article._sort_key = published_dt or datetime.min
			new_articles.append(article)

	new_articles.sort(key=lambda a: getattr(a, "_sort_key", datetime.min), reverse=True)
	for a in new_articles:
		if hasattr(a, "_sort_key"):
			delattr(a, "_sort_key")

	if new_articles:
		save_cache(new_articles)

	logger.info(
		"Retrieved %d new articles for topic %s", len(new_articles), topic.upper()
	)
	return TopicList(topic, new_articles)


def check_cache(entry: Article) -> bool:
	"""
	Return True if the article title is not already in the cache.
	"""
	title_to_check = entry.title.strip()
	for cached in load_cache():
		existing_title = cached.title.strip()
		if title_to_check == existing_title:
			return False
	return True


def save_cache(articles: List[Article]) -> None:
	"""
	Add new articles to the JSON cache as {title: published_string}.
	"""
	cache_path = Path(__file__).resolve().parents[1] / CACHE_FILE
	current: dict[str, str] = {}

	if cache_path.exists():
		try:
			with cache_path.open("r", encoding="utf-8") as f:
				current = json.load(f)
		except JSONDecodeError:
			current = {}

	for a in articles:
		# use title as the unique key
		current[a.title.strip()] = a.publish_time

	cache_path.parent.mkdir(parents=True, exist_ok=True)
	with cache_path.open("w", encoding="utf-8") as f:
		json.dump(current, f, ensure_ascii=False, indent=2)


def load_cache() -> List[HeadlineCache]:
	"""
	Load cached headlines and return a list of HeadlineCache objects,
	keyed by title.
	"""
	cache_path = Path(__file__).resolve().parents[1] / CACHE_FILE
	cached_entries: List[HeadlineCache] = []
	if cache_path.exists():
		try:
			with cache_path.open("r", encoding="utf-8") as f:
				cached_json = json.load(f)
			for title, published_str in cached_json.items():
				# HeadlineCache stores published and identifier (here: title)
				cached_entries.append(HeadlineCache(published_str, title.strip()))
		except JSONDecodeError as e:
			logger.warning("Cache file unreadable: %s (%s)", cache_path, e)
	return cached_entries

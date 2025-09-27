"""
main.py is the entry point for headline_scraper.
"""
from src import setup_logging
from src.config import TOPICS
from src.emailer import send_email
from src.format import to_html
from src.scrape import get_articles_for_all

import logging
logger = logging.getLogger(__name__)

def main():
	"""
	Scrapes Google for RSS entries corresponding to
	user-defined topic keywords and emails them to specified recipients.
	:return: None
	"""
	setup_logging()
	logger.info(f"Scraping headlines for {TOPICS}")
	feed = get_articles_for_all(TOPICS)
	html_contents = to_html(feed)
	send_email(html_contents)


# TODO: Setup daily script run
# TODO: Add when article published to source HTML
# TODO: Cache headlines for three days to avoid repetition
# TODO: Make CSS formatting nicer


if __name__ == "__main__":
	main()

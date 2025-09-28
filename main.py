"""
main.py is the entry point for headline_scraper.
"""

import logging

from src import setup_logging
from src.config import TOPICS
from src.emailer import send_email
from src.format import to_html
from src.scrape import get_articles_for_all

logger = logging.getLogger(__name__)


def main():
    """
    Scrapes Google for RSS entries corresponding to
    user-defined topic keywords and emails them to specified recipients.
    :return: None
    """
    setup_logging(default_path=None)
    logger.info(f"Scraping headlines for {TOPICS}")
    feed = get_articles_for_all(TOPICS)
    html_contents = to_html(feed)
    send_email(html_contents)


# TODO: Setup daily script run
# TODO: Make CSS formatting nicer
# TODO: cache email sending data and newsletter count


if __name__ == "__main__":
    main()

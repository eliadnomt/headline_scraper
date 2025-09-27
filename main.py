"""
main.py is the entry point for headline_scraper.
"""

from src.config import TOPICS
from src.emailer import send_email
from src.format import to_html
from src.scrape import get_articles_for_all


def main():
    """
    Scrapes Google for RSS entries corresponding to
    user-defined topic keywords and emails them to specified recipients.
    :return: None
    """
    feed = get_articles_for_all(TOPICS)
    html_contents = to_html(feed)
    send_email(html_contents)


# TODO: Setup daily script run
# TODO: Implement logging
# TODO: Cache headlines for three days to avoid repetition
# TODO: Make CSS formatting nicer


if __name__ == "__main__":
    main()

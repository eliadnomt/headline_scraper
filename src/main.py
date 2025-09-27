"""
main.py is the entry point for headline_scraper.
"""

from email import send_email

from config import TOPICS
from format import to_html
from scrape import get_articles_for_all


def main():
    """
    Scrapes Google for RSS entries corresponding to
    user-defined topic keywords and emails them to specified recipients.
    :return: None
    """
    feed = get_articles_for_all(TOPICS)
    html_contents = to_html(feed)
    send_email(html_contents)


if __name__ == "__main__":
    main()

from emailer import send_email
from formatter import to_html
from scraper import get_articles_for_all
from config import TOPICS

def main():
	feed = get_articles_for_all(TOPICS)
	html_contents = to_html(feed)
	send_email(html_contents)

if __name__ == "__main__":
	main()

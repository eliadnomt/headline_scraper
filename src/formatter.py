from typing import List

from helpers import TopicList


def to_html(feed: List[TopicList]) -> str:
    html = "<h1>quoi de neuf</h1>"

    for topic in feed:
        html += f"<h2>{topic.title}</h2>"
        for article in topic.article_list:
            html += f"<p><a href='{article.link}'>{article.title}</a><br>{article.description}</p>"
    return html

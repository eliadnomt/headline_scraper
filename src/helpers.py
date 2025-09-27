from dataclasses import dataclass
from typing import List


@dataclass
class Article:
	title: str
	link: str
	description: str


@dataclass
class TopicList:
	title: str
	article_list: list


@dataclass
class Email:
	subject: str
	body: str
	recipients: List[str]
	server: str
	port: int

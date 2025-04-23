
import re
from typing import List
from abc import ABC, abstractmethod
from dataclasses import dataclass

from feedparser.util import FeedParserDict

from .keywords import AbstractKeywordExtractor


def grab_arxiv_code_from_link(url):
    match_obj = re.match(r'http[s]?://*arxiv.org/(abs|pdf)/([\d\w\.]+)', url)
    if match_obj is None:
        raise ValueError('Invalid arXiv link!')
    return match_obj[2]


class DataVersionError(Exception):
    def __init__(self, given_version, class_version):
        self.given_version = given_version
        self.class_version = class_version

    def __str__(self):
        return "Wrong data version. Given version: {given:}, but this class version: {correct:}".format(
            given=self.given_version,
            correct=self.class_version
        )


class AbstractArticleEntry(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @property
    @abstractmethod
    def data_version(self) -> str:
        pass


@dataclass
class BasicArticleEntry(AbstractArticleEntry):
    arxiv_code: str
    title: str
    authors: List[str]
    publish_time: str
    abstract: str
    arxiv_url: str
    pdf_url: str
    primary_category: str
    tags: List[str]

    def to_dict(self) -> dict:
        return {
            'data_version': self.data_version,
            'arxiv_code': self.arxiv_code,
            'title': self.title,
            'authors': self.authors,
            'publish_time': self.publish_time,
            'abstract': self.abstract,
            'arxiv_url': self.arxiv_url,
            'pdf_url': self.pdf_url,
            'primary_category': self.primary_category,
            'tags': self.tags
        }

    @property
    def data_version(self) -> str:
        return '2025-03-23'

    @property
    def summary(self) -> str:
        return self.abstract

    @classmethod
    def make_entry_from_feed(cls, feed_entry: FeedParserDict) -> AbstractArticleEntry:
        title = feed_entry.title
        authors = [author.name for author in feed_entry.authors]
        publish_time = feed_entry.published
        abstract = feed_entry.summary.replace('\n', ' ')
        arxiv_url = feed_entry.link
        pdf_url = ''
        for links_item in feed_entry.links:
            if links_item.type == 'application/pdf':
                pdf_url = links_item.href
                break
        primary_category = feed_entry.arxiv_primary_category['term']
        tags = [item['term'] for item in feed_entry.tags]
        arxiv_code = grab_arxiv_code_from_link(arxiv_url)

        return BasicArticleEntry(
            arxiv_code=arxiv_code,
            title=title,
            authors=authors,
            publish_time=publish_time,
            abstract=abstract,
            arxiv_url=arxiv_url,
            pdf_url=pdf_url,
            primary_category=primary_category,
            tags=tags
        )

    @classmethod
    def make_entry_from_dict(cls, entry_dict: dict) -> AbstractArticleEntry:
        if 'data_version' not in entry_dict.keys():
            return BasicArticleEntry(**entry_dict)
        elif entry_dict['data_version'] != '2025-03-23':
            raise DataVersionError(entry_dict['data_version'], '2025-03-23')
        else:
            return BasicArticleEntry(**{k: v for k, v in entry_dict.items() if k != 'data_version'})


@dataclass
class ArticleEntryWithKeywords(BasicArticleEntry):
    keywords: List[str]

    def set_keywords(self, keywords: List[str]):
        self.keywords = keywords

    def to_dict(self) -> dict:
        return {
            'data_version': self.data_version,
            'arxiv_code': self.arxiv_code,
            'title': self.title,
            'authors': self.authors,
            'publish_time': self.publish_time,
            'abstract': self.abstract,
            'arxiv_url': self.arxiv_url,
            'pdf_url': self.pdf_url,
            'primary_category': self.primary_category,
            'tags': self.tags,
            'keywords': self.keywords
        }

    @property
    def data_version(self) -> str:
        return '2025-04-03'

    @classmethod
    def make_entry_from_feed(cls, feed_entry: FeedParserDict) -> AbstractArticleEntry:
        title = feed_entry.title
        authors = [author.name for author in feed_entry.authors]
        publish_time = feed_entry.published
        abstract = feed_entry.summary.replace('\n', ' ')
        arxiv_url = feed_entry.link
        pdf_url = ''
        for links_item in feed_entry.links:
            if links_item.type == 'application/pdf':
                pdf_url = links_item.href
                break
        primary_category = feed_entry.arxiv_primary_category['term']
        tags = [item['term'] for item in feed_entry.tags]
        arxiv_code = grab_arxiv_code_from_link(arxiv_url)
        keywords = []

        return ArticleEntryWithKeywords(
            arxiv_code=arxiv_code,
            title=title,
            authors=authors,
            publish_time=publish_time,
            abstract=abstract,
            arxiv_url=arxiv_url,
            pdf_url=pdf_url,
            primary_category=primary_category,
            tags=tags,
            keywords=[]
        )

    @classmethod
    def make_entry_from_dict(cls, entry_dict: dict) -> AbstractArticleEntry:
        if 'data_version' not in entry_dict.keys():
            return BasicArticleEntry(**entry_dict)
        elif entry_dict['data_version'] != '2025-04-03':
            raise DataVersionError(entry_dict['data_version'], '2025-04-03')
        else:
            return ArticleEntryWithKeywords(**{k: v for k, v in entry_dict.items() if k != 'data_version'})

    @classmethod
    def make_entry_by_adding_keywords(cls, entry: BasicArticleEntry, keyword_extractor: AbstractKeywordExtractor) -> AbstractArticleEntry:
        keyword_prob_pairs = keyword_extractor.extract_keywords(entry.abstract)
        entry_dict = entry.to_dict()
        entry_dict['keywords'] = [keyword for keyword, _ in keyword_prob_pairs]
        entry_dict['data_version'] = '2025-04-03'
        return ArticleEntryWithKeywords.make_entry_from_dict(entry_dict)

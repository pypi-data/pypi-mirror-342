
import urllib.request
from typing import List

import feedparser
from feedparser.util import FeedParserDict

from .data import AbstractArticleEntry, BasicArticleEntry


base_url = 'http://export.arxiv.org/api/query?'



class ArXivExtractor:
    def __init__(self, nb_articles_each_turn: int=100):
        self._nb_articles_each_turn = nb_articles_each_turn

    def _raw_retrieve_articles_api(self, dts: str, start: int, max_results: int) -> FeedParserDict:
        query = 'search_query=submittedDate:[{dts:}0000+TO+{dts:}2359]&start={start:}&max_results={max_results:}&sortBy=submittedDate&sortOrder=ascending'.format(
            dts=dts,
            start=start,
            max_results=max_results
        )

        url = base_url + query

        response = urllib.request.urlopen(url).read()
        return feedparser.parse(response)

    def _partial_retrieve_articles(self, dts: str, start: int=0, max_results: int=None) -> List[AbstractArticleEntry]:
        if max_results is None:
            max_results = self._nb_articles_each_turn
        feed = self._raw_retrieve_articles_api(dts, start, max_results)

        article_entries = []
        for entry in feed.entries:
            article_entry = BasicArticleEntry.make_entry_from_feed(entry)
            article_entries.append(article_entry)

        return article_entries

    def retrieve_all_articles_given_date(self, dts: str) -> List[AbstractArticleEntry]:
        article_entries = []
        all_retrieved = False
        start_idx = 0
        while not all_retrieved:
            this_article_entries = self._partial_retrieve_articles(
                dts,
                start=start_idx,
                max_results=self._nb_articles_each_turn
            )
            article_entries += this_article_entries
            if len(this_article_entries) < self._nb_articles_each_turn:
                all_retrieved = True
            else:
                start_idx += self._nb_articles_each_turn
        return article_entries

    @property
    def nb_articles_each_turn(self) -> int:
        return self._nb_articles_each_turn

    @nb_articles_each_turn.setter
    def nb_articles_each_turn(self, val: int):
        self._nb_articles_each_turn = val

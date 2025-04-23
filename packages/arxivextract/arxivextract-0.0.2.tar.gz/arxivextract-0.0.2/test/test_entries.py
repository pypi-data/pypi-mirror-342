
import unittest

from arxivextract.extraction import ArXivExtractor
from arxivextract.data import AbstractArticleEntry, BasicArticleEntry, ArticleEntryWithKeywords
from arxivextract.keywords import make_keyword_extractor, AbstractKeywordExtractor, KeywordBertKeywordExtractor


class TestEntries(unittest.TestCase):
    def setUp(self):
        self.extractor = ArXivExtractor()

    def test_entry(self):
        results = self.extractor.retrieve_all_articles_given_date('20111231')
        assert len(results) == 117
        assert results[0].arxiv_code == '1201.0200v2'
        assert results[0].arxiv_url == 'http://arxiv.org/abs/1201.0200v2'
        assert results[0].pdf_url == 'http://arxiv.org/pdf/1201.0200v2'
        assert results[0].primary_category == 'quant-ph'
        assert results[0].data_version == '2025-03-23'

        result_dict = results[0].to_dict()
        assert isinstance(result_dict, dict)
        assert result_dict['data_version'] == '2025-03-23'
        assert 'quant-ph' in result_dict['tags']

    def test_dict_to_entry(self):
        dictentry = {
            'data_version': '2025-03-23',
            'arxiv_code': '1201.0200v2',
            'title': 'Gaussian matrix-product states for coding in bosonic communication\n  channels',
            'authors': ['Joachim Schäfer', 'Evgueni Karpov', 'Nicolas J. Cerf'],
            'publish_time': '2011-12-31T00:03:33Z',
            'abstract': 'The communication capacity of Gaussian bosonic channels with memory has recently attracted much interest. Here, we investigate a method to prepare the multimode entangled input symbol states for encoding classical information into these channels. In particular, we study the usefulness of a Gaussian matrix product state (GMPS) as an input symbol state, which can be sequentially generated although it remains heavily entangled for an arbitrary number of modes. We show that the GMPS can achieve more than 99.9% of the Gaussian capacity for Gaussian bosonic memory channels with a Markovian or non-Markovian correlated noise model in a large range of noise correlation strengths. Furthermore, we present a noise class for which the GMPS is the exact optimal input symbol state of the corresponding channel. Since GMPS are ground states of particular quadratic Hamiltonians, our results suggest a possible link between the theory of quantum communication channels and quantum many-body physics.',
            'arxiv_url': 'http://arxiv.org/abs/1201.0200v2',
            'pdf_url': 'http://arxiv.org/pdf/1201.0200v2',
            'primary_category': 'quant-ph',
            'tags': ['quant-ph']
        }
        entry = BasicArticleEntry.make_entry_from_dict(dictentry)
        assert isinstance(entry, BasicArticleEntry)
        assert isinstance(entry, AbstractArticleEntry)
        assert entry.title == dictentry['title']
        assert 'Evgueni Karpov' in entry.authors
        assert entry.data_version == '2025-03-23'

    def test_keyword_entry_from_dict(self):
        dictentry = {
            'data_version': '2025-03-23',
            'arxiv_code': '1201.0200v2',
            'title': 'Gaussian matrix-product states for coding in bosonic communication\n  channels',
            'authors': ['Joachim Schäfer', 'Evgueni Karpov', 'Nicolas J. Cerf'],
            'publish_time': '2011-12-31T00:03:33Z',
            'abstract': 'The communication capacity of Gaussian bosonic channels with memory has recently attracted much interest. Here, we investigate a method to prepare the multimode entangled input symbol states for encoding classical information into these channels. In particular, we study the usefulness of a Gaussian matrix product state (GMPS) as an input symbol state, which can be sequentially generated although it remains heavily entangled for an arbitrary number of modes. We show that the GMPS can achieve more than 99.9% of the Gaussian capacity for Gaussian bosonic memory channels with a Markovian or non-Markovian correlated noise model in a large range of noise correlation strengths. Furthermore, we present a noise class for which the GMPS is the exact optimal input symbol state of the corresponding channel. Since GMPS are ground states of particular quadratic Hamiltonians, our results suggest a possible link between the theory of quantum communication channels and quantum many-body physics.',
            'arxiv_url': 'http://arxiv.org/abs/1201.0200v2',
            'pdf_url': 'http://arxiv.org/pdf/1201.0200v2',
            'primary_category': 'quant-ph',
            'tags': ['quant-ph']
        }

        keyword_extractor = make_keyword_extractor('2025-04-02-keyword')
        assert isinstance(keyword_extractor, AbstractKeywordExtractor)
        assert isinstance(keyword_extractor, KeywordBertKeywordExtractor)
        basic_entry = BasicArticleEntry.make_entry_from_dict(dictentry)
        assert isinstance(basic_entry, AbstractArticleEntry)
        assert isinstance(basic_entry, BasicArticleEntry)
        assert basic_entry.data_version == '2025-03-23'
        keyword_entry = ArticleEntryWithKeywords.make_entry_by_adding_keywords(basic_entry, keyword_extractor)
        assert isinstance(keyword_entry, AbstractArticleEntry)
        assert isinstance(keyword_entry, ArticleEntryWithKeywords)
        assert isinstance(keyword_entry, BasicArticleEntry)
        assert keyword_entry.data_version == '2025-04-03'


if __name__ == '__main__':
    unittest.main()


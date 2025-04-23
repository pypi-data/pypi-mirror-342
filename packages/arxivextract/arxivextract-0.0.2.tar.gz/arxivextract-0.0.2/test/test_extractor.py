
import unittest

from arxivextract.extraction import ArXivExtractor
from arxivextract.data import AbstractArticleEntry, BasicArticleEntry


class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = ArXivExtractor(nb_articles_each_turn=100)

    def test_partial_extract_1(self):
        # test partial run
        results = self.extractor._partial_retrieve_articles('20250401', start=0, max_results=10)
        assert len(results) == 10
        assert isinstance(results[0], AbstractArticleEntry)
        assert isinstance(results[0], BasicArticleEntry)
        assert results[1].data_version == '2025-03-23'
        assert results[0].arxiv_code == '2504.02863v1'
        assert results[0].arxiv_url == 'http://arxiv.org/abs/2504.02863v1'
        assert results[0].pdf_url == 'http://arxiv.org/pdf/2504.02863v1'
        assert results[0].primary_category == 'cs.CL'

    def test_partial_extract_2(self):
        results = self.extractor._partial_retrieve_articles('20250401', start=10, max_results=20)
        assert len(results) == 20
        assert isinstance(results[5], AbstractArticleEntry)
        assert isinstance(results[15], BasicArticleEntry)
        assert results[10].data_version == '2025-03-23'
        assert results[0].arxiv_code == '2504.00306v1'
        assert results[0].arxiv_url == 'http://arxiv.org/abs/2504.00306v1'
        assert results[0].pdf_url == 'http://arxiv.org/pdf/2504.00306v1'
        assert results[0].primary_category == 'cs.LG'

    def test_full_extraction(self):
        # full extraction
        results = self.extractor.retrieve_all_articles_given_date('20250401')
        assert len(results) == 985
        assert isinstance(results[85], AbstractArticleEntry)
        assert isinstance(results[515], BasicArticleEntry)
        assert results[100].primary_category == 'astro-ph.HE'

    def test_turnnb(self):
        self.extractor.nb_articles_each_turn = 23
        assert self.extractor.nb_articles_each_turn == 23

        self.extractor.nb_articles_each_turn = 106
        assert self.extractor.nb_articles_each_turn == 106

        self.extractor.nb_articles_each_turn = 100
        assert self.extractor.nb_articles_each_turn == 100


if __name__ == '__main__':
    unittest.main()


from abc import ABC, abstractmethod

from keybert import KeyBERT


class AbstractKeywordExtractor(ABC):
    @abstractmethod
    def extract_keywords(self, text: str) -> list[str]:
        pass


class KeywordBertKeywordExtractor(AbstractKeywordExtractor):
    def __init__(self, config: dict, embed_model='all-MiniLM-L6-v2'):
        self._keyword_model = KeyBERT(model=embed_model)
        self._config = config

    def extract_keywords(self, text: str) -> list[str]:
        return self._keyword_model.extract_keywords(text, **self._config)

    @property
    def keywordbertmodel(self) -> KeyBERT:
        return self._keyword_model


keyword_configs = {
    '2025-04-02-keyword': {
        'model': 'KeyBERT',
        'embed_model': 'all-MiniLM-L6-v2',
        'configs': {
            'keyphrase_ngram_range': (1, 3),
            'stop_words': 'english',
            'top_n': 5
        }
    }
}


def make_keyword_extractor(version: str) -> AbstractKeywordExtractor:
    if version not in keyword_configs.keys():
        raise ValueError('Keyword version {} is not found.'.format(version))

    keyword_extraction_model = keyword_configs[version].get('model')
    if keyword_extraction_model is None:
        raise ValueError('NoneType error!')
    if keyword_extraction_model == 'KeyBERT':
        return KeywordBertKeywordExtractor(
            keyword_configs[version].get('configs'),
            embed_model=keyword_configs[version].get('embed_model', 'all-MiniLM-L6-v2')
        )
    else:
        raise ValueError('Unknown keyword extraction model: {}'.format(keyword_extraction_model))

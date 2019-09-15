from abc import ABC, abstractmethod
from typing import Callable, List

from common.corpus import Corpus

class FeatureExtractor(ABC):
    
    def __init__(self, corpus: Corpus):
        super().__init__()
        self.corpus = corpus

    @abstractmethod
    def _word_cmp_key(self) -> Callable[[str], List[str]]:
        pass

    def get_feature_words(self, num_features: int = 30) -> [str]:
        return sorted(self.corpus.vocabulary, key=self._word_cmp_key(), reverse=True)[:num_features]


class MostFrequentWordsExtractor(FeatureExtractor):

    def __init__(self, corpus: Corpus):
        super().__init__(corpus)

    def _word_cmp_key(self) -> Callable[[str], List[str]]:
        return (lambda word: self.corpus.vocabulary[word].freq)
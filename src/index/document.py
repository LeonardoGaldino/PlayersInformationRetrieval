from functools import reduce
from abc import ABC, abstractmethod

from utils import tokenizer

class BaseDocument(ABC):

    @abstractmethod
    def get_terms(self) -> [str]:
        pass

    def get_term_frequency(self, term: str) -> int:
        return self.get_terms().count(term)

    def get_most_frequent_term(self) -> (int, str):
        terms_freq = list(map(lambda term: (self.get_term_frequency(term), term), self.get_terms()))
        terms_freq.sort()
        return terms_freq[-1]

    def get_tf(self, term: str) -> float:
        occurrences = self.get_term_frequency(term)
        (most_freq, _) = self.get_most_frequent_term()

        return (0.5 + (0.5*occurrences)/most_freq)


class QueryDocument(BaseDocument):

    def __init__(self, query: str):
        self.query = query

    def get_terms(self) -> [str]:
        return [token.lower() for token in tokenizer.tokenize(self.query)]


class IndexDocument(BaseDocument):

    def __init__(self, _id: int, _json: dict = None):
        self.id = _id
        self.raw = _json

        if _json is not None:
            self._pre_process()

    def _pre_process(self):
        if self.raw is None:
            return

        self.url = self.raw.get('url', None)
        if self.url is None:
            raise KeyError("Tried to load a document that does not contain an URL. Id = {}".format(self.id))

        self.name = self.raw.get('name', None)
        self.number = self.raw.get('number', None)
        self.position = self.raw.get('position', None)
        self.nationality = self.raw.get('nationality', None)
        self.team = self.raw.get('team', None)
        self.foot = self.raw.get('foot', None)

    def get_terms(self):
        tokenized_text = list(map(tokenizer.tokenize, [self.name, self.number, self.position, self.nationality, self.team, self.foot]))
        flat_tokens = reduce(lambda acc, v: acc+v, tokenized_text, [])
        return [token.lower() for token in flat_tokens]

    


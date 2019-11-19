from functools import reduce, total_ordering
from abc import ABC, abstractmethod
from math import sqrt

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

        return (0.5 + (0.5*occurrences)/(1.0 + most_freq))


class DocumentVector:

    def __init__(self, doc: BaseDocument, index):
        self.doc = doc
        self.index = index
        self.project(self)

    def dot_product(self, other) -> float:
        if not isinstance(other, DocumentVector):
            raise TypeError("Trying to compute dot product with parameter that is not a DocumentVector.")

        if self.dim != other.dim:
            raise TypeError("Trying to compute similarity between vectors of different size.")

        return reduce(lambda acc, vs: acc+ vs[0]*vs[1], list(zip(self.v, other.v)), 0.0)

    def norm(self) -> float:
        return sqrt(reduce(lambda acc, v: acc + v*v, self.v, 0.0))

    def similarity(self, other) -> float:
        if not isinstance(other, DocumentVector):
            raise TypeError("Trying to compute similarity with parameter that is not a DocumentVector.")

        if self.dim != other.dim:
            raise TypeError("Trying to compute similarity between vectors of different size.")

        return self.dot_product(other)/(1.0 + self.norm() + other.norm())

    def project(self, other):
        if not isinstance(other, DocumentVector):
            raise TypeError("Trying to project vector with parameter that is not a DocumentVector.")

        terms = other.doc.get_terms()

        self.dim = len(terms)
        self.v = [self.doc.get_tf(term)*self.index.get_idf(term) for term in terms]

    @total_ordering
    def __lt__(self, other):
        return True


class QueryDocument(BaseDocument):

    def __init__(self, query: str = None, terms: [str] = None):
        if terms is not None: 
            self.query = ' '.join(terms)
        else:
            self.query = query

    def get_terms(self) -> [str]:
        return [token.lower() for token in tokenizer.tokenize(self.query, True)]


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
        self.text = self.raw.get('text', None)

    def get_terms(self):
        tokenized_text = list(map(tokenizer.tokenize, [self.name, self.number, self.position, self.nationality, self.team, self.foot]))
        flat_tokens = reduce(lambda acc, v: acc+v, tokenized_text, [])
        return [token.lower() for token in flat_tokens]

    


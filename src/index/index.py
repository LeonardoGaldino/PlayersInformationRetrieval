import os.path
from os import path
import json

from math import log
from functools import reduce
from index.document import IndexDocument, QueryDocument, DocumentVector
from index.utils import map_number_to_range
from utils.tokenizer import tokenize

import nltk
from nltk.corpus import stopwords as nltk_stopwords

nltk.download('stopwords')
stopwords = nltk_stopwords.words('english')

class Index:

    """Index types:
    1 - (String) Frequency index without optimization
    2 - (String) Frequency index with gap compression optimization
    3 - (Binary) """
    def __init__(self):
        self.index ={}
        self.data = None
        self.type = 0

    def load_data(self):
        with open("docs_file.json", "r") as file:
            self.data = json.load(file)

    def load(self):
        index_file = None
        self.load_data()

        if path.exists("index/freq_index.txt"):
            index_file = open("index/freq_index.txt", "r")
            self.type = 1
            self.load_freq_index(index_file)

    def load_freq_index(self, file):
        for line in file:
            field = line.split("//")[0]
            vocabulary = line.split("//")[1]
            words = vocabulary.split()

            if not field in self.index:
                self.index[field] = {}

            word = words[0]
            frequency = int(words[1])

            self.index[field][word] = {}
            self.index[field][word] = {'freq': frequency, 'postings': []}

            words.pop(0)
            words.pop(0)

            for doc in words:
                doc = doc.split(":")
                self.index[field][word]["postings"].append((int(doc[0]), int(doc[1])))

    def get_document(self, _id: int) -> IndexDocument:
        return IndexDocument(_id-1, self.data[_id - 1])

    def get_documents(self, ids: [int]) -> [IndexDocument]:
        return [self.get_document(_id) for _id in ids]

    def corpus_size(self) -> int:
        return len(self.data)

    def get_idf(self, term: str) -> float:
        postings = list(map(lambda field: self.find(field, term)[1], self.index.keys()))
        postings = reduce(lambda acc, v: acc+list(map(lambda doc_entry: doc_entry[0], v)), postings, [])
        occurrences = list(set(postings))
        
        return log(1 + float(self.corpus_size())/float(1+len(occurrences)))

    def find(self, field: str, term: str) -> (int, list):
        if field == 'number':
            try:
                term = map_number_to_range(int(term))
            except:
                pass
        
        data = self.index[field][term] if (field in self.index) and (term in self.index[field]) else {"freq": 0, "postings": []}
        freq = data["freq"]
        postings = data["postings"]

        return freq, postings

    def find_documents(self, field: str, term: str) -> [IndexDocument]:
        postings = self.find(field, term)[1]
        return self.get_documents([posting[0] for posting in postings])

    def get_documents_for_query(self, field: str, query: str, tf_idf: bool = True) -> [IndexDocument]:
        # Separa cada termo da consulta
        terms = tokenize(query.lower(), True)

        # Remove stopwords da consulta
        if field != 'foot':
            terms = list(filter(lambda term: not term in stopwords, terms))

        # Busca todos os documentos para cada termo da consulta
        docs = [self.find_documents(field, term) for term in terms]

        # Deixa a lista de documentos flat, i.e., em uma lista (antes numa matriz)
        docs = reduce(lambda acc, v: acc+v, docs, [])

        # Remove documentos duplicados
        docs = list(set(docs))

        # Transforma cada documento em um vetor
        docs_vectors = [DocumentVector(doc, self) for doc in docs]

        # Transforma termos da consulta no documento da consulta
        query_doc = QueryDocument(None, terms)

        # Transforma o documento da consulta em um vetor no espaço da consulta
        query_vector = DocumentVector(query_doc, self)
        query_vector.project(query_vector, tf_idf)


        # Para cada vetor de documento, projetamos ele no espaço da consulta
        for doc_vector in docs_vectors:
            doc_vector.project(query_vector, tf_idf)

        # Computamos a similiridade com o vetor de consulta de cada documento e associamos ao mesmo documento para recupera-los depois
        docs_score_vectors = [(query_vector.similarity(doc_vector), doc_vector) for doc_vector in docs_vectors]

        # Ordenamos de acordo com o score (crescente)
        docs_score_vectors.sort()

        # Invertemos a ordem dos documentos para ter docs com scores altos primeiro
        docs_score_vectors.reverse()

        # Descartamos o score e ficamos somente com os documentos
        return [d[1].doc for d in docs_score_vectors]


if __name__ == "__main__":
    i = Index()
    i.load()
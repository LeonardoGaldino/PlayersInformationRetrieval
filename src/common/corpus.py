from common.document import Document

class Corpus:

    def __init__(self, documents: [Document]):
        self.documents = documents
        self._build_corpus_vocabulary()

    def _build_corpus_vocabulary(self):
        self.vocabulary = {}
        doc_index = 0
        for document in self.documents:
            for token in document.vocabulary:
                freq = document.vocabulary[token]
                stats = self.vocabulary.get(token, None)
                if stats is None:
                    self.vocabulary[token] = CorpusTokenStats(freq, [doc_index])
                else:
                    self.vocabulary[token].add_stats(freq, doc_index)

            doc_index += 1



class CorpusTokenStats:

    def __init__(self, freq: int = 0, docs: [int] = []):
        self.freq = freq
        self.docs = docs

    def add_stats(self, freq: int, doc: int):
        self.freq += freq
        self.docs.append(doc)

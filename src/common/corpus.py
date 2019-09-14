from common.document import Document

class Corpus:

    def __init__(self, documents: [Document]):
        self.documents = documents
        self._build_corpus_vocabulary()

    # Precomputa o vocabulário e suas estatísticas
    def _build_corpus_vocabulary(self):
        self.vocabulary = {}
        doc_index = 0

        for document in self.documents:
            for token in document.vocabulary:
                # Frequência da palavra <token> no documento sendo analisado
                freq = document.vocabulary[token]

                # Checa se o vocabulário do corpus já contém a palavra
                stats = self.vocabulary.get(token, None)

                # Caso não, cria com a frequência do doc atual e adiciona seu índice
                if stats is None:
                    self.vocabulary[token] = CorpusTokenStats(freq, [doc_index])
                # Caso sim, adiciona a frequência do doc atual e seu índice
                else:
                    self.vocabulary[token].add_stats(freq, doc_index)

            doc_index += 1


# Classe responsável por representar as estatísticas de uma palavra dentro do corpus
# Atualmente guarda a frequência total de ocorrências daquela palavra e os documentos nos quais apareceu
class CorpusTokenStats:

    def __init__(self, freq: int = 0, docs: [int] = []):
        self.freq = freq
        self.docs = docs

    def add_stats(self, freq: int, doc: int):
        self.freq += freq
        self.docs.append(doc)

from common.document import Document, DocumentClass

from nltk.corpus import stopwords as nltk_stopwords
import nltk

nltk.download('stopwords')


# Classe responsável por representar as estatísticas de uma palavra dentro do corpus
# Atualmente guarda a frequência total de ocorrências daquela palavra e os documentos nos quais apareceu
class CorpusTokenStats:

    def __init__(self):
        self.data = {
            DocumentClass.INSTANCE.value: {
                'freq': 0,
                'docs': [],
            },
            DocumentClass.NON_INSTANCE.value: {
                'freq': 0,
                'docs': [],
            },
        }

    def add_stats(self, freq: int, doc: int, is_instance: DocumentClass):
        self.data[is_instance.value]['freq'] += freq
        self.data[is_instance.value]['docs'].append(doc)

    def get_total_freq(self) -> int:
        return self.data[DocumentClass.INSTANCE.value]['freq'] + self.data[DocumentClass.NON_INSTANCE.value]['freq']

    def get_all_docs(self) -> [int]:
        return self.data[DocumentClass.INSTANCE.value]['docs'] + self.data[DocumentClass.NON_INSTANCE.value]['docs']

class Corpus:

    def __init__(self, documents: [Document]):
        self.documents = documents
        self._build_corpus_vocabulary()

    # Precomputa o vocabulário e suas estatísticas
    def _build_corpus_vocabulary(self):
        self.vocabulary = {}
        doc_index = 0
        stemmer = nltk.stem.porter.PorterStemmer()

        for document in self.documents:
            for token in document.vocabulary:
                # Frequência da palavra <token> no documento sendo analisado
                freq = document.vocabulary[token]

                lower_token = token.lower()
                stemmed_lower_token = stemmer.stem(lower_token)

                # Checa se o vocabulário do corpus já contém a palavra
                stats = self.vocabulary.get(stemmed_lower_token, None)

                # Caso não, cria com a frequência do doc atual e adiciona seu índice
                if stats is None:
                    self.vocabulary[stemmed_lower_token] = CorpusTokenStats()

                self.vocabulary[stemmed_lower_token].add_stats(freq, doc_index, document.is_instance)

            doc_index += 1

    # Dropa stopwords em ingles definidas pelo package nltk
    # Pode retornar um novo corpus cujo vocabulário não contém stopwords
    # Ou pode retornar o mesmo corpus com o vocabulário sem stopwords
    def drop_stop_words(self, in_place: bool = True):
        return_corpus = self
        if not in_place:
            return_corpus = Corpus(self.documents)

        for stop_word in nltk_stopwords.words('english'):
            try:
                del return_corpus.vocabulary[stop_word]
            except KeyError:
                pass

        return return_corpus

    def vocabulary_get(self, word: str) -> CorpusTokenStats:
        stats = self.vocabulary.get(word, None)
        if stats is None:
            self.vocabulary[word] = CorpusTokenStats()
        return self.vocabulary[word]

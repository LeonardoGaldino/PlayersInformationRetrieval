import requests
import bs4

from src.utils.http_status import OK
from src.utils.tokenizer import tokenize

class Document:

    def __init__(self, raw_doc: str):
        self.raw_doc = raw_doc
        self._build_doc_vocabulary()

    def _build_doc_vocabulary(self):
        parser = bs4.BeautifulSoup(self.raw_doc, 'html.parser')

        clean_up_tags = ['script', 'style']

        for tag_name in clean_up_tags:
            for tag in parser(tag_name):
                tag.extract()

        anchor_texts = []
        non_breaking_space = '\xa0'
        for anchor in parser('a'):
            anchor_text = anchor.string
            if anchor_text is not None and len(anchor_text) > 1 and anchor_text != non_breaking_space:
                anchor_texts.append(anchor_text)
            anchor.extract()

        doc_text = parser.get_text()
        doc_words = tokenize(doc_text)
        
        anchor_words = [tokenize(anchor_text) for anchor_text in anchor_texts]
        flatten_words = [item for sublist in anchor_words for item in sublist]

        doc_words = doc_words + flatten_words

        self.vocabulary = {}
        for word in doc_words:
            word_freq = self.vocabulary.get(word, 0)
            self.vocabulary[word] = word_freq + 1


    @staticmethod
    def load_from_url(url: str):
        req = requests.get(url)
        if req.status_code == OK:
            return Document(req.content.decode('utf-8'))
        return None


    
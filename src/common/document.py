import requests
import bs4

from utils.http_status import OK
from utils.tokenizer import tokenize

class Document:

    def __init__(self, raw_doc: str, is_instance: bool):
        self.raw_doc = raw_doc
        self.is_instance = is_instance
        self._build_doc_vocabulary()

    # Função interna do documento responsável por transformar o documento cru (html com todas as tags e textos)
    # Em um vocabulário com frequência de palavras
    def _build_doc_vocabulary(self):
        # Instancia o HTML parser do BeautifulSoup
        parser = bs4.BeautifulSoup(self.raw_doc, 'html.parser')

        # Tags que vão ser removidas do documento
        # Não queremos nem script (js) nem style (css) pois não agregam informações
        clean_up_tags = ['script', 'style']

        for tag_name in clean_up_tags:
            for tag in parser(tag_name):
                # Remove uma tag do documento
                tag.extract()


        # Remove âncoras mas guarda seus textos
        anchor_texts = []
        non_breaking_space = '\xa0'
        for anchor in parser('a'):
            anchor_text = anchor.string
            if anchor_text is not None and len(anchor_text) > 1 and anchor_text != non_breaking_space:
                anchor_texts.append(anchor_text)
            anchor.extract()

        # Pega texto do documento resultante das operações acima
        doc_text = parser.get_text()

        # Tokeniza (ver função tokenize)
        doc_words = tokenize(doc_text)
        
        # Tokeniza o texto de cada âncora removida
        anchor_words = [tokenize(anchor_text) for anchor_text in anchor_texts]

        # Transforma em uma única lista, pois antes era uma matriz
        # (Eram várias âncoras, cada uma foi tokenizada, logo, matriz 2D)
        flatten_words = [item for sublist in anchor_words for item in sublist]

        # Junta tokens do documento com tokens das âncoras removidas
        doc_words = doc_words + flatten_words

        # Inicializa vocabulário do documento
        # (É um mapeamento de palavras e sua frequência no documento)
        self.vocabulary = {}

        # Faz a contagem
        for word in doc_words:
            word_freq = self.vocabulary.get(word, 0)
            self.vocabulary[word] = word_freq + 1


    # Método apenas para auxiliar a construção de um Documento a partir de uma URL.
    @staticmethod
    def load_from_url(url: str, is_instance: bool):
        req = requests.get(url)
        if req.status_code == OK:
            return Document(req.content.decode('utf-8'), is_instance)
        return None


    
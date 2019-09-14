import os

from utils.corpus_loader import load_corpus

# Por enquanto, apenas testa o corpus
if __name__ == '__main__':
    cd = os.getcwd()
    d = os.path.join(cd, 'samples_pages')
    corpus = load_corpus(d)
    for token in corpus.vocabulary:
        print(token, corpus.vocabulary[token].freq, len(corpus.vocabulary[token].docs))
    print(len(corpus.vocabulary))
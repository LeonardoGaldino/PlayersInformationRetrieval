import os

from utils.corpus_loader import load_corpus

if __name__ == '__main__':
    cd = os.getcwd()
    d = os.path.join(cd, 'samples_pages')
    corpus = load_corpus(d)
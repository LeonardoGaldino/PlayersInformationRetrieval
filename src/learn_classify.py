import os

from utils.corpus_loader import load_corpus
from classifier.features_extractors import MostFrequentWordsExtractor, DocFrequencyDifferenceExtractor, PlainFrequencyDifferenceExtractor, MixedFrequencyDifferenceExtractor

# Por enquanto, apenas testa o corpus
if __name__ == '__main__':
    cd = os.getcwd()
    inst_dir = os.path.join(cd, 'samples_pages')
    non_inst_dir = os.path.join(cd, 'nonsamples_pages')
    corpus = load_corpus(inst_dir, non_inst_dir).drop_stop_words(in_place=True)

    for token in corpus.vocabulary:
        occurrences = len(corpus.vocabulary[token].get_all_docs())
        total_docs = len(corpus.documents)
        if total_docs*.4 < occurrences:
            pass
            #print("{} = {}".format(token, occurrences))

    selector = MostFrequentWordsExtractor(corpus)
    selector2 = DocFrequencyDifferenceExtractor(corpus)
    selector3 = PlainFrequencyDifferenceExtractor(corpus)
    selector4 = MixedFrequencyDifferenceExtractor(corpus)

    feature_words = selector.get_feature_words()
    feature_words2 = selector2.get_feature_words()
    feature_words3 = selector3.get_feature_words()
    feature_words4 = selector4.get_feature_words()

    print("MostFrequentWordsExtractor: {}".format(feature_words))
    print()
    print("DocFrequencyDifferenceExtractor: {}".format(feature_words2))
    print()
    print("PlainFrequencyDifferenceExtractor: {}".format(feature_words3))
    print()
    print("MixedFrequencyDifferenceExtractor: {}".format(feature_words4))
    print()

    fv, y = corpus.documents[0].get_feature_vector(feature_words)
    fv2, y2 = corpus.documents[0].get_feature_vector(feature_words2)
    fv3, y3 = corpus.documents[0].get_feature_vector(feature_words3)
    fv4, y4 = corpus.documents[0].get_feature_vector(feature_words4)

    _fv, _y = corpus.documents[95].get_feature_vector(feature_words)
    _fv2, _y2 = corpus.documents[95].get_feature_vector(feature_words2)
    _fv3, _y3 = corpus.documents[95].get_feature_vector(feature_words3)
    _fv4, _y4 = corpus.documents[95].get_feature_vector(feature_words4)
    print(fv, y)
    print(fv2, y2)
    print(fv3, y3)
    print(fv4, y4)
    print(_fv, _y)
    print(_fv2, _y2)
    print(_fv3, _y3)
    print(_fv4, _y4)
    print()
    print(len(list(filter(lambda v: v.is_instance, corpus.documents))))
    print(len(list(filter(lambda v: not v.is_instance, corpus.documents))))

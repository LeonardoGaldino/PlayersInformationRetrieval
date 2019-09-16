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
    print("MostFrequentWordsExtractor: {}".format(selector.get_feature_words()))
    print()
    print("DocFrequencyDifferenceExtractor: {}".format(selector2.get_feature_words()))
    print()
    print("PlainFrequencyDifferenceExtractor: {}".format(selector3.get_feature_words()))
    print()
    print("MixedFrequencyDifferenceExtractor: {}".format(selector4.get_feature_words()))
    print()
    print(len(list(filter(lambda v: v.is_instance, corpus.documents))))
    print(len(list(filter(lambda v: not v.is_instance, corpus.documents))))

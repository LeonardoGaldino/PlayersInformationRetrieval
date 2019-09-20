import os

from utils.corpus_loader import load_corpus
from classifier.features_extractors import MostFrequentWordsExtractor, DocFrequencyDifferenceExtractor, PlainFrequencyDifferenceExtractor, MixedFrequencyDifferenceExtractor
from classifier.mlp import MLPDocumentClassifier, MLPDocClassifier

# Por enquanto, apenas testa o corpus
if __name__ == '__main__':
    cd = os.getcwd()
    inst_dir = os.path.join(cd, 'samples_pages')
    non_inst_dir = os.path.join(cd, 'nonsamples_pages')
    corpus = load_corpus(inst_dir, non_inst_dir).drop_stop_words(in_place=True)

    print('\nFrequent words:')
    for token in corpus.vocabulary:
        occurrences = len(corpus.vocabulary[token].get_all_docs())
        total_docs = len(corpus.documents)
        if total_docs*.4 < occurrences:
            print("{} = {}".format(token, occurrences))

    selector = MostFrequentWordsExtractor(corpus)
    selector2 = DocFrequencyDifferenceExtractor(corpus)
    selector3 = PlainFrequencyDifferenceExtractor(corpus)
    selector4 = MixedFrequencyDifferenceExtractor(corpus)

    n_features = 50
    feature_words = selector.get_feature_words(n_features)
    feature_words2 = selector2.get_feature_words(n_features)
    feature_words3 = selector3.get_feature_words(n_features)
    feature_words4 = selector4.get_feature_words(n_features)

    print('')
    print("MostFrequentWordsExtractor: {}".format(feature_words))
    print()
    print("DocFrequencyDifferenceExtractor: {}".format(feature_words2))
    print()
    print("PlainFrequencyDifferenceExtractor: {}".format(feature_words3))
    print()
    print("MixedFrequencyDifferenceExtractor: {}".format(feature_words4))
    print()

    '''print("AllExtractors:")
    MLPDocumentClassifier(corpus).train([feature_words, feature_words2, feature_words3, feature_words4], verbose=True)

    print("MostFreq + DocDiff + Mixed DifferenceExtractors:")
    MLPDocumentClassifier(corpus).train([feature_words, feature_words2, feature_words4], verbose=True)

    print("DocDiff + Mixed Extractors:")
    MLPDocumentClassifier(corpus).train([feature_words2, feature_words4], verbose=True)

    print("DocDifferenceExtractor:")
    MLPDocumentClassifier(corpus).train([feature_words2], verbose=True)

    print("MixedFrequencyDifferenceExtractor:")
    MLPDocumentClassifier(corpus).train([feature_words4], verbose=True)'''

    print("New MLP:")
    MLPDocClassifier(selector2).train(corpus.documents, train_size=.8, verbose=True)


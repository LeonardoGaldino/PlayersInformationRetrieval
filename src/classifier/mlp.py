from datetime import datetime as dt

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle
from sklearn import preprocessing

from common.corpus import Corpus
from common.document import Document, DocumentClass
from classifier.classifier import Classifier
from classifier.features_extractors import FeatureExtractor
from classifier.utils import print_metrics, doc_class_to_int, int_to_doc_class, get_vectors, get_vectors_scaler

class MLPDocumentClassifier(Classifier):

    def __init__(self, feature_extractor: FeatureExtractor):
        super().__init__(feature_extractor)
        self.trained = False

    def train(self, docs: [Document], train_size: float = 1.0, verbose: bool = False):
        start_time = dt.now()

        positive_docs = list(filter(lambda doc: doc.is_instance == DocumentClass.INSTANCE, docs))
        negative_docs = list(filter(lambda doc: not doc.is_instance == DocumentClass.INSTANCE, docs))

        total_positive = int(len(positive_docs)*train_size)
        total_negative = int(len(negative_docs)*train_size)

        train_docs = positive_docs[:total_positive] + negative_docs[:total_negative]
        train_docs = shuffle(train_docs)

        test_docs = positive_docs[total_positive:] + negative_docs[total_negative:]
        test_docs = shuffle(test_docs)

        self.features = self.feature_extractor.get_feature_words(num_features=50)
        clf = MLPClassifier(hidden_layer_sizes=(len(self.features), len(self.features)), activation='relu', solver='adam', max_iter=1000)


        parameters = {'solver': ('adam', 'lbfgs', 'sgd'), 'activation': ('relu', 'identity', 'tanh', 'logistic'), 'learning_rate_init': (0.001, 0.005, 0.01)}
        clf = GridSearchCV(clf, parameters, scoring='accuracy', verbose=1)

        self.clf = clf

        X, y, self.scaler = get_vectors_scaler(self.features, train_docs)

        self.clf.fit(X, y)

        if len(test_docs) > 0:
            final_preds = self._internal_predict(test_docs)
            final_preds = doc_class_to_int(final_preds)
            correct_preds = doc_class_to_int([test_doc.is_instance for test_doc in test_docs])

            if verbose:
                print_metrics(final_preds, correct_preds)

        if verbose:
            end_time = dt.now()
            train_duration = (end_time-start_time).total_seconds()
            print("Training took {} seconds".format(train_duration))
        self.trained = True

    def predict(self, docs: [Document]) -> [DocumentClass]:
        if not self.trained:
            raise AssertionError("MLP not trained yet. Call train before predict.")

        X, _ = get_vectors(self.features, docs, self.scaler)
        preds = self.clf.predict(X)
        return int_to_doc_class(preds)

    def predict_proba(self, docs: [Document]) -> [float]:
        if not self.trained:
            raise AssertionError("MLP not trained yet. Call train before predict.")

        X, _ = get_vectors(self.features, docs, self.scaler)
        preds = self.clf.predict_proba(X)
        return preds

    # Bypass predict trained check for usage inside train method
    def _internal_predict(self, docs: [Document]) -> [DocumentClass]:
        temp = self.trained
        self.trained = True

        result = self.predict(docs)

        self.trained = temp
        return result


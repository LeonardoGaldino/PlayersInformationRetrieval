from sklearn.neural_network import MLPClassifier
from sklearn.utils import shuffle
from sklearn import preprocessing

from common.corpus import Corpus
from common.document import Document, DocumentClass

class MLPDocumentClassifier:

    def __init__(self, corpus: Corpus):
        self.corpus = corpus
        self.scaler = preprocessing.StandardScaler()

    def _get_vectors(self, feature_words: [str], docs: [Document], training: bool) -> ([float], [int]):
        vectors = [doc.get_feature_vector(feature_words) for doc in docs]
        X, y = [vector[0] for vector in vectors], [vector[1] for vector in vectors]

        if training:
            self.scaler.fit(X)

        X = self.scaler.transform(X)
        y = [label.value for label in y]
        return X, y

    def train(self, features: [[str]], corpus_train_size: float = .8):
        positive_docs = list(filter(lambda doc: doc.is_instance == DocumentClass.INSTANCE, self.corpus.documents))
        negative_docs = list(filter(lambda doc: not doc.is_instance == DocumentClass.INSTANCE, self.corpus.documents))

        total_positive = len(positive_docs)
        total_negative = len(negative_docs)

        positive_train_size = int(total_positive*corpus_train_size)

        negative_train_size = int(total_negative*corpus_train_size)

        train_docs = positive_docs[:positive_train_size] + negative_docs[:negative_train_size]
        train_docs = shuffle(train_docs)

        test_docs = positive_docs[positive_train_size:] + negative_docs[negative_train_size:]
        test_docs = shuffle(test_docs)

        X_train0, y_train0 = self._get_vectors(features[0], train_docs, True)
        X_test0, y_test0 = self._get_vectors(features[0], test_docs, False)

        X_train1, y_train1 = self._get_vectors(features[1], train_docs, True)
        X_test1, y_test1 = self._get_vectors(features[1], test_docs, False)

        clf0 = MLPClassifier(hidden_layer_sizes=(30,30,30), activation='relu', solver='adam', max_iter=1000)
        clf0.fit(X_train0, y_train0)

        clf1 = MLPClassifier(hidden_layer_sizes=(30,30,30), activation='relu', solver='adam', max_iter=1000)
        clf1.fit(X_train1, y_train1)

        score0 = clf0.score(X_test0, y_test0)
        score1 = clf1.score(X_test1, y_test1)

        print(score0, score1)

        probs0 = clf0.predict_proba(X_test0)
        probs1 = clf1.predict_proba(X_test1)

        preds = []
        for i in range(len(probs0)):
            p0, l0 = (probs0[i][0], 0) if probs0[i][0] > probs0[i][1] else (probs0[i][1], 1)
            p1, l1 = (probs1[i][0], 0) if probs1[i][0] > probs1[i][1] else (probs1[i][1], 1)

            if p0 > p1:
                preds.append(l0)
            else:
                preds.append(l1)

        err = 0
        for i in range(len(preds)):
            err += abs(preds[i] - y_test0[i])
        print(err, len(preds))
        print(1.0 - float(err)/float(len(preds)))








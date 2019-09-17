from datetime import datetime as dt

from sklearn.neural_network import MLPClassifier
from sklearn.utils import shuffle
from sklearn import preprocessing

from common.corpus import Corpus
from common.document import Document, DocumentClass

class MLPDocumentClassifier:

    def __init__(self, corpus: Corpus):
        self.corpus = corpus

    def _get_vectors(self, feature_words: [str], docs: [Document], training: bool, index: int) -> ([float], [int]):
        vectors = [doc.get_feature_vector(feature_words) for doc in docs]
        X, y = [vector[0] for vector in vectors], [vector[1] for vector in vectors]

        if training:
            self.clf_data[index]['scaler'] = preprocessing.StandardScaler().fit(X)

        X = self.clf_data[index]['scaler'].transform(X)
        y = [label.value for label in y]
        return X, y

    def compute_metrics(self, y_pred: [int], y: [int]):
        mat = [[0,0], [0,0]]
        p = 0
        f = 0
        for i in range(len(y)):
            p += 1 if y[i] == 1 else 0
            f += 1 if y[i] == 0 else 0
            if y_pred[i] == y[i]:
                label = 0 if y[i] == 0 else 1
                mat[label][label] += 1
            else:
                mat[y_pred[i]][y[i]] += 1
        tp, tn, fp, fn = mat[1][1], mat[0][0], mat[1][0], mat[0][1]

        acc = float(tp+tn)/float(f+p)
        prec = float(tp)/float(tp+fp)
        recall = float(tp)/float(p)
        f1m = 2*prec*recall/(prec+recall)
        return (mat, acc, prec, recall, f1m)


    def train(self, features: [[str]], corpus_train_size: float = .7, verbose: bool = False):
        start_time = dt.now()
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

        self.clf_data = []
        test_data = []

        for i in range(len(features)):
            self.clf_data.append({})
            X_train, y_train = self._get_vectors(features[i], train_docs, True, i)
            X_test, y_test = self._get_vectors(features[i], test_docs, False, i)
            n_features = len(features[i])
            
            self.clf_data[i]['clf'] = MLPClassifier(hidden_layer_sizes=(n_features, n_features), activation='relu', solver='adam', max_iter=1000)
            self.clf_data[i]['clf'].fit(X_train, y_train)
            self.clf_data[i]['features'] = features[i]

            test_data.append((X_test, y_test))

        for i in range(len(self.clf_data)):
            score = self.clf_data[i]['clf'].score(test_data[i][0], test_data[i][1])
            if verbose:
                print('Classifier {} individual accuracy: {}'.format(i+1, score))

        final_preds = self.predict(test_docs)

        if verbose:
            err = 0
            for i in range(len(final_preds)):
                err += abs(final_preds[i] - test_data[0][1][i])
            print("\nFinal stats:")
            print("{} errors in {} samples".format(err, len(final_preds)))
            mat, acc, prec, recall, f1m = self.compute_metrics(final_preds, test_data[0][1])
            print("Confusion matrix: ")
            print(mat[0])
            print(mat[1])
            print("Accuracy: {}".format(acc))
            print("Precision: {}".format(prec))
            print("Recall: {}".format(recall))
            print("F1-Measure: {}".format(f1m))
            print("")
            end_time = dt.now()
            train_duration = (end_time-start_time).total_seconds()
            print("Training took {} seconds".format(train_duration))


    def predict(self, docs: [Document]) -> [int]:
        if self.clf_data is None:
            raise AttributeError("Classificator not trained. Call train method before predict!")
        
        predicts = []
        for i in range(len(self.clf_data)):
            clf = self.clf_data[i]['clf']
            features = self.clf_data[i]['features']
            X, _ = self._get_vectors(features, docs, False, i)

            predicts.append(clf.predict_proba(X))

        final_preds = []
        for i in range(len(docs)):
            p, sum_prob_p = 0, 0.0
            f, sum_prob_f = 0, 0.0
            for j in range(len(predicts)):
                sum_prob_p += predicts[j][i][1]
                sum_prob_f += predicts[j][i][0]
                if predicts[j][i][0] > predicts[j][i][1]:
                    f += 1
                else:
                    p += 1
            tie = p == f
            if tie:
                final_preds.append(1 if sum_prob_p > sum_prob_f else 0)
            else:
                final_preds.append(1 if p > f else 0)

        return final_preds



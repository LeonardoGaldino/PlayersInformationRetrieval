from sklearn.preprocessing import StandardScaler

from common.document import Document, DocumentClass

def get_vectors(feature_words: [str], docs: [Document], scaler: StandardScaler = None) -> ([float], [int]):
    vectors = [doc.get_feature_vector(feature_words) for doc in docs]
    X, y = [vector[0] for vector in vectors], [vector[1] for vector in vectors]

    if scaler is not None:
        X = scaler.transform(X)

    y = [label.value for label in y]
    return X, y

def get_vectors_scaler(feature_words: [str], docs: [Document]) -> ([float], [int], StandardScaler):
    vectors = [doc.get_feature_vector(feature_words) for doc in docs]
    X, y = [vector[0] for vector in vectors], [vector[1] for vector in vectors]
    scaler = StandardScaler().fit(X)

    X = scaler.transform(X)
    y = [label.value for label in y]
    return X, y, scaler

def doc_class_to_int(classes: [DocumentClass]):
    return [1 if _cls == DocumentClass.INSTANCE else 0 for _cls in classes]

def int_to_doc_class(classes: [int]):
    return [DocumentClass.INSTANCE if _cls == 1 else DocumentClass.NON_INSTANCE for _cls in classes]

def compute_metrics(y_pred: [int], y: [int]):
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
    tp, tn, fp = mat[1][1], mat[0][0], mat[1][0]

    acc = float(tp+tn)/float(f+p)
    prec = float(tp)/float(tp+fp)
    recall = float(tp)/float(p)
    f1m = 2*prec*recall/(prec+recall)
    return (mat, acc, prec, recall, f1m)

def print_metrics(y_pred: [int], y: [int]):
    print("Metrics:")
    mat, acc, prec, recall, f1m = compute_metrics(y_pred, y)
    print("Confusion matrix: ")
    print(mat[0])
    print(mat[1])
    print("Accuracy: {}".format(acc))
    print("Precision: {}".format(prec))
    print("Recall: {}".format(recall))
    print("F1-Measure: {}".format(f1m))
from abc import ABC, abstractmethod

from common.document import Document, DocumentClass
from classifier.features_extractors import FeatureExtractor


class Classifier(ABC):

    def __init__(self, feature_extractor: FeatureExtractor):
        super().__init__()
        self.feature_extractor = feature_extractor

    @abstractmethod
    def train(self, docs: [Document]):
        pass

    @abstractmethod
    def predict(self, docs: [Document]) -> [DocumentClass]:
        pass

class AccuracyWeightedEnsemble:

    def __init__(self, classifiers: [Classifier]):
        self.classifiers = classifiers
        self.trained = False

    def train(self, docs: [Document]):
        # TODO: Train each classifier and check their accuracy for later weighting
        self.trained = True

    def predict(self, docs: [Document]) -> [DocumentClass]:
        if not self.trained:
            raise AssertionError("Ensemble not trained yet. Call train before predict.")
        # TODO: Use each trained classifier 
        return []
        
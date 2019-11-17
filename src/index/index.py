import os.path
from os import path
import json


class Index:

    """Index types:
    1 - (String) Frequency index without optimization
    2 - (String) Frequency index with gap compression optimization
    3 - (Binary) """
    def __init__(self):
        self.index ={}
        self.data = None
        self.type = 0

    def load_data(self):
        with open("src/docs_file.json", "r") as file:
            self.data = json.load(file)

    def load(self):
        index_file = None
        self.load_data()

        if path.exists("src/index/freq_index.txt"):
            index_file = open("src/index/freq_index.txt", "r")
            self.type = 1
            self.load_freq_index(index_file)

    def load_freq_index(self, file):
        c = 0
        for line in file:
            field = line.split("//")[0]
            vocabulary = line.split("//")[1]
            words = vocabulary.split()

            if not field in self.index:
                self.index[field] = {}

            word = words[0]
            frequency = int(words[1])

            self.index[field][word] = {}
            self.index[field][word] = {'freq': frequency, 'postings': []}

            words.pop(0)
            words.pop(0)

            for doc in words:
                self.index[field][word]["postings"].append(int(doc))

    def get_document(self, position: int) -> dict:
        return self.data[position - 1]

    def find(self, field: str, term: str) -> (int, list):
        freq = self.index[field][term]["freq"]
        postings = self.index[field][term]["postings"]

        return (freq, postings)


if __name__ == "__main__":
    i = Index()
    i.load()
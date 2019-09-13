from os import listdir
from os.path import isfile, join

from src.common.corpus import Corpus
from src.common.document import Document

# Function responsible for loading corpus from a given folder.
# You should input an absolute path to a folder containing all documents.
def load_corpus(folder_path: str) -> Corpus:
    files = [file for file in listdir(folder_path) if isfile(join(folder_path, file))]
    documents = []
    for file in files:
        file_path = join(folder_path, file)
        with open(file_path, 'r') as document:
            doc = Document(document.read())
            documents.append(doc)

    return Corpus(documents)
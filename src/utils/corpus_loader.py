from os import listdir
from os.path import isfile, join

from common.corpus import Corpus
from common.document import Document, DocumentClass

# Function responsible for loading corpus from a given folder.
# You should input an absolute path to a folder containing all documents.
def load_corpus(instance_folder_path: str, non_instance_folder_path: str) -> Corpus:
    files = [(file, DocumentClass.INSTANCE) for file in listdir(instance_folder_path) if isfile(join(instance_folder_path, file))] \
        + [(file, DocumentClass.NON_INSTANCE) for file in listdir(non_instance_folder_path) if isfile(join(non_instance_folder_path, file))]
    documents = []
    for file, is_instance in files:
        folder_path = instance_folder_path if is_instance == DocumentClass.INSTANCE else non_instance_folder_path
        file_path = join(folder_path, file)
        with open(file_path, 'r') as document:
            doc = Document(document.read(), is_instance)
            documents.append(doc)

    return Corpus(documents)

def load_documents(folder_path: str) -> [Document]:
    files = [file for file in listdir(folder_path) if isfile(join(folder_path, file))]

    documents = []
    for file in files:
        with open(join(folder_path, file), 'r') as document:
            doc = Document(document.read(), DocumentClass.UNKNOWN)
            documents.append(doc)

    return documents
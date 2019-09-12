from os import listdir
from os.path import isfile, join

def load_documents(folder_path: str) -> [str]:
    files = [file for file in listdir(folder_path) if isfile(join(folder_path, file))]
    documents = []
    for file in files:
        file_path = join(folder_path, file)
        with open(file_path, 'r') as document:
            documents.append(document.read())

    return documents
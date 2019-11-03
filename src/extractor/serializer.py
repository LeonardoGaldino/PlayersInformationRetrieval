import os
from wrappers.eurosport_wrapper import EurosportWrapper

class Serializer:

    def __init__(self, extractors: [], dirs: []):
        self.extractors = extractors
        self.dirs = dirs
        self.entities = []

    def extract_entities(self):
        for i in range(len(self.extractors)):
            for entry in os.scandir(self.dirs[i]):
                try:
                    self.entities.append(extractors[i].extract_player_entity(entry.path).copy())
                except:
                    pass


if __name__ == '__main__':
    extractor = EurosportWrapper()
    extractors = [extractor]
    path_to_dir = "../crawler/pagesHeuristica/Eurosport"
    directories = [path_to_dir]
    serial = Serializer(extractors, directories)
    serial.extract_entities()
    print(serial.entities)
    print('Quantidade de entidades: ' + str(len(serial.entities)))
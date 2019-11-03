import os
import json
from wrappers.eurosport_wrapper import EurosportWrapper
from wrappers.uefa_wrapper import UefaWrapper
from wrappers.fctables_wrapper import FCTablesWrapper
from wrappers.fbref_wrapper import FbrefWrapper
from wrappers.fifa_wrapper import FifaWrapper
from wrappers.soccerway_wrapper import SoccerWayWrapper
from wrappers.mlssoccer_wrapper import MLSSoccerWrapper

class Serializer:

    def __init__(self, extractors: [], dirs: []):
        self.extractors = extractors
        self.dirs = dirs
        self.entities = []

    def extract_entities(self):
        j = 0
        for i in range(len(self.extractors)):
            for entry in os.scandir(self.dirs[i]):
                j += 1
                try:
                    path = entry.path.replace("..", "/src")
                    entity = extractors[i].extract_player_entity(entry.path).copy()
                    entity["path"] = path
                    self.entities.append(entity)
                    if j % 100 == 0:
                        print(self.entities[j])
                except:
                    pass


if __name__ == '__main__':
    extractors = []
    extractor1 = EurosportWrapper()
    extractor2 = UefaWrapper()
    extractor3 = FCTablesWrapper()
    extractor4 = FbrefWrapper()
    #extractor = FifaWrapper() #ESTA COM ERRO
    extractor5 = SoccerWayWrapper()
    extractor6 = MLSSoccerWrapper()

    extractors.append(extractor1)
    extractors.append(extractor2)
    extractors.append(extractor3)
    extractors.append(extractor4)
    extractors.append(extractor5)
    extractors.append(extractor6)

    directories = []
    path_to_dir1 = "../crawler/pagesHeuristica/Eurosport"
    path_to_dir2 = "../crawler/pagesHeuristica/UEFA"
    path_to_dir3 = "../crawler/pagesHeuristica/FCTable"
    path_to_dir4 = "../crawler/pagesHeuristica/Fbref"
    #path_to_dir = "../crawler/pagesHeuristica/FIFA" #ESTA COM ERRO
    path_to_dir5 = "../crawler/pagesHeuristica/Soccerway"
    path_to_dir6 = "../crawler/pagesHeuristica/MLSSoccer"

    directories.append(path_to_dir1)
    directories.append(path_to_dir2)
    directories.append(path_to_dir3)
    directories.append(path_to_dir4)
    directories.append(path_to_dir5)
    directories.append(path_to_dir6)

    serial = Serializer(extractors, directories)
    serial.extract_entities()

    with open("../docs_file.json", "w") as write_file:
        json.dump(serial.entities, write_file)

    print('Quantidade de entidades: ' + str(len(serial.entities)))
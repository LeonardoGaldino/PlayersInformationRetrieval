import os
import json
from typing import List, Any

from wrappers.eurosport_wrapper import EurosportWrapper
from wrappers.uefa_wrapper import UefaWrapper
from wrappers.fctables_wrapper import FCTablesWrapper
from wrappers.fbref_wrapper import FbrefWrapper
from wrappers.soccerway_wrapper import SoccerWayWrapper
from wrappers.mlssoccer_wrapper import MLSSoccerWrapper

class Serializer:

    def __init__(self, extractors: [], dirs: []):
        self.extractors = extractors
        self.dirs = dirs
        self.entities = None

    def extract_entities(self):
        self.entities = []
        j = 0
        for i in range(len(self.extractors)):
            for entry in os.scandir(self.dirs[i]):
                j += 1
                try:
                    entity = extractors[i].extract_player_entity(entry.path).copy()
                    self.entities.append(entity)
                except:
                    pass


if __name__ == '__main__':
    extractors = []
    extractor1 = EurosportWrapper()
    extractor2 = UefaWrapper()
    extractor3 = FCTablesWrapper()
    extractor4 = FbrefWrapper()
    extractor5 = SoccerWayWrapper()
    extractor6 = MLSSoccerWrapper()

    extractors.append(extractor1)
    extractors.append(extractor2)
    extractors.append(extractor3)
    extractors.append(extractor4)
    extractors.append(extractor5)
    extractors.append(extractor6)

    directories = []
    path_to_dir1 = "../crawler/pagesComURL/Eurosport"
    path_to_dir2 = "../crawler/pagesComURL/UEFA"
    path_to_dir3 = "../crawler/pagesComURL/FCTable"
    path_to_dir4 = "../crawler/pagesComURL/Fbref"
    path_to_dir5 = "../crawler/pagesComURL/Soccerway"
    path_to_dir6 = "../crawler/pagesComURL/MLSSoccer"

    directories.append(path_to_dir1)
    directories.append(path_to_dir2)
    directories.append(path_to_dir3)
    directories.append(path_to_dir4)
    directories.append(path_to_dir5)
    directories.append(path_to_dir6)

    serial = Serializer(extractors, directories)
    serial.extract_entities()
    print(serial.entities["position"].keys())
    with open("../docs_file.json", "w") as write_file:
        json.dump(serial.entities, write_file)

    print('Quantidade de entidades: ' + str(len(serial.entities)))
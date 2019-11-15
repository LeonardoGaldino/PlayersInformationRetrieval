import json
import os
import re

COUNTRIES = {'BRA': 'Brazil',
             'FRA': 'France',
             'ESP': 'Spain',
             'TUR': 'Turkey',
             'CRO': 'Croatia',
             'SUI': 'Switzerland',
             'WAL': 'Wales',
             'CZE': 'Czech Republic',
             'BEL': 'Belgium',
             'SRB': 'Serbia',
             'GER': 'Germany',
             'BFA': 'Burkina Faso',
             'POL': 'Poland',
             'ARG': 'Argentina',
             'JPN': 'Japan',
             'KOR': 'Korea',
             'POR': 'Portugal',
             'NED': 'Netherlands',
             'ITA': 'Italy',
             'URU': 'Uruguay',
             'ZAM': 'Zambia',
             'COD': 'Congo',
             'BIH': 'Bosnia and Herzegovina',
             'MAR': 'Morocco',
             'ENG': 'England',
             'AUT': 'Austria',
             'RUS': 'Russia',
             'CHI': 'China',
             'IRL': 'Ireland',
             'USA': 'United States of America',
             'COL': 'Colombia',
             'UKR': 'Ukraine',
             'CIV': 'Cote d\'Ivoire',
             'SEN': 'Senegal',
             'CRC': 'Costa Rica',
             'MLI': 'Mali',
             'GRE': 'Greece',
             'SVK': 'Slovakia',
             'IRN': 'Iran',
             'ALG': 'Algeria',
             'CAN': 'Canada',
             'GAM': 'Gambia',
             'DEN': 'Denmark',
             'GEO': 'Georgia',
             'HUN': 'Hungary',
             'ANG': 'Angola',
             'ROU': 'Romania',
             'MNE': 'Montenegro',
             'VEN': 'Venezuela',
             'BHR': 'Bahrain',
             'GHA': 'Ghana',
             'LUX': 'Luxembourg',
             'SCO': 'Scotland',
             'MEX': 'Mexico',
             'NOR': 'Norway',
             'NGA': 'Nigeria',
             'MKD': 'Macedonia',
             'SWE': 'Sweden',
             'ALB': 'Albania',
             'CMR': 'Cameroon',
             'AUS': 'Australia',
             'FIN': 'Finland',
             'MOZ': 'Mozambique',
             'KEN': 'Kenya',
             'EGY': 'Egypt',
             'TAN': 'Tanzania',
             'SVN': 'Slovenia',
             'ISR': 'Israel',
             'TUN': 'Tunisia',
             'JAM': 'Jamaica',
             'LVA': 'Latvia',
             'GNB': 'Guinea-Bissau',
             'RSA': 'South Africa',
             'NZL': 'New Zealand',
             'GUI': 'Guinea',
             'GAB': 'Gabon',
             'GUY': 'Guyana'
             }

class FrequencyIndex:

    def __init__(self):
        self.index = {}
        self.index["name"] = {}
        self.index["position"] = {}
        self.index["nationality"] = {}
        self.index["team"] = {}
        self.index["number"] = {}
        self.index["foot"] = {}
        self.index["terms"] = {}
        self.size = 0

    def create_from_json(self):
        with open("../docs_file.json", "r") as file:
            self.data = json.load(file)

        for entity in self.data:
            if 'name' in entity:
                self.add_name_entry(entity['name'], self.data.index(entity) + 1)

            if 'position' in entity:
                self.add_position_entity(entity['position'], self.data.index(entity) + 1)

            if 'nationality' in entity:
                self.add_nationality_entity(entity['nationality'], self.data.index(entity) + 1)

            if 'foot' in entity:
                self.add_foot_entity(entity['foot'], self.data.index(entity) + 1)

            if 'team' in entity:
                self.add_team_entity(entity['team'], self.data.index(entity) + 1)

            if 'number' in entity:
                self.add_number_entity(entity['number'], self.data.index(entity) + 1)

            if 'text' in entity:
                pass

    def load_index(self):
        pass

    def save_index(self):
        txt = ''
        for i in self.index.keys():
            txt += i + '\n'
            for j in self.index[i].keys():
                txt += j + ' ' + str(self.index[i][j]['freq'])
                for p in self.index[i][j]['postings']:
                    txt += ' ' + str(p)
                txt += '\n'

        with open ('freq_index.txt', 'w') as file:
            file.write(txt)

    def add_name_entry (self, name: str, pos: int):
        names = name.split()
        for n in names:
            if n in self.index['name']:
                self.index['name'][n]['freq'] += 1
                self.index['name'][n]['postings'].append(pos)
            else:
                self.index['name'][n] = {}
                self.index['name'][n]['freq'] = 1
                self.index['name'][n]['postings'] = [pos]

    def add_position_entity(self, position: str, pos: int):
        if '-' in position:
            positions = position.split('-')
        elif '/' in position:
            positions = position.split('/')
        else:
            positions = [position]

        for p in positions:
            if p == 'Attack' or p == 'FW' or p == 'Forward' or p == 'WM':
                p = 'Attacker'
            elif p == 'MF' or p == 'Midfield':
                p = 'Midfielder'
            elif p == 'GK':
                p = 'Goalkeeper'
            elif p == 'DF' or p == 'Defence':
                p = 'Defender'
            elif p == '':
                continue
            else:
                pass

            if p in self.index['position']:
                self.index['position'][p]['freq'] += 1
                self.index['position'][p]['postings'].append(pos)
            else:
                self.index['position'][p] = {}
                self.index['position'][p]['freq'] = 1
                self.index['position'][p]['postings'] = [pos]

    def add_nationality_entity(self, nationality: str, pos: int):
        if len(nationality) == 3:
            nationality = COUNTRIES[nationality]

        words = nationality.split()
        for w in words:
            if w in self.index['nationality']:
                self.index['nationality'][w]['freq'] += 1
                self.index['nationality'][w]['postings'].append(pos)
            else:
                self.index['nationality'][w] = {}
                self.index['nationality'][w]['freq'] = 1
                self.index['nationality'][w]['postings'] = [pos]

    def add_foot_entity(self, foot: str, pos: int):
        if foot in self.index['foot']:
            self.index['foot'][foot]['freq'] += 1
            self.index['foot'][foot]['postings'].append(pos)
        else:
            self.index['foot'][foot] = {}
            self.index['foot'][foot]['freq'] = 1
            self.index['foot'][foot]['postings'] = [pos]

    def add_team_entity(self, team: str, pos: int):
        words = team.split()
        for w in words:
            if w in self.index['team']:
                self.index['team'][w]['freq'] += 1
                self.index['team'][w]['postings'].append(pos)
            else:
                self.index['team'][w] = {}
                self.index['team'][w]['freq'] = 1
                self.index['team'][w]['postings'] = [pos]

    def add_number_entity(self, number: int, pos: int):
        num = str(number)
        if num in self.index['number']:
            self.index['number'][num]['freq'] += 1
            self.index['number'][num]['postings'].append(pos)
        else:
            self.index['number'][num] = {}
            self.index['number'][num]['freq'] = 1
            self.index['number'][num]['postings'] = [pos]

    def add_text_entity(self, text: str, pos: int):
        pass


if __name__ == '__main__':
    index = FrequencyIndex()
    index.create_from_json()
    index.save_index()
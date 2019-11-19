import json
import nltk

from index.utils import map_number_to_range

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
        self.index = {"name": {}, "position": {}, "nationality": {}, "team": {}, "number": {}, "foot": {}, "term": {}}
        self.data = None
        self.size = 0

    def create_from_json(self):
        with open("docs_file.json", "r") as file:
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

            self.add_text_entity(entity, self.data.index(entity) + 1)

            self.size += 1

    def load_index(self):
        pass

    def get_doc(self, i: int) -> dict:
        return self.data[i - 1]

    def save_index(self):
        txt = ''
        for i in self.index.keys():
            for j in self.index[i].keys():
                txt += i + "//" + str(j) + ' ' + str(self.index[i][j]['freq'])
                for p in self.index[i][j]['postings']:
                    txt += ' ' + str(p[0]) + ":" + str(p[1])
                txt += '\n'

        with open('index/freq_index.txt', 'w') as file:
            file.write(txt)

    def add_name_entry(self, name: str, id: int):
        name = name.lower()
        names = name.split()
        for n in names:
            if n in self.index['name']:
                self.index['name'][n]['freq'] += 1
                self.index['name'][n]['postings'].append((id, 1))
            else:
                self.index['name'][n] = {}
                self.index['name'][n]['freq'] = 1
                self.index['name'][n]['postings'] = [(id, 1)]

    def add_position_entity(self, position: str, id: int):
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

            p = p.lower()
            if p in self.index['position']:
                self.index['position'][p]['freq'] += 1
                self.index['position'][p]['postings'].append((id, 1))
            else:
                self.index['position'][p] = {}
                self.index['position'][p]['freq'] = 1
                self.index['position'][p]['postings'] = [(id, 1)]

    def add_nationality_entity(self, nationality: str, id: int):
        if len(nationality) == 3:
            nationality = COUNTRIES[nationality]

        nationality = nationality.lower()
        words = nationality.split()
        for w in words:
            if w in self.index['nationality']:
                self.index['nationality'][w]['freq'] += 1
                self.index['nationality'][w]['postings'].append((id, 1))
            else:
                self.index['nationality'][w] = {}
                self.index['nationality'][w]['freq'] = 1
                self.index['nationality'][w]['postings'] = [(id, 1)]

    def add_foot_entity(self, foot: str, id: int):
        foot = foot.lower()
        if foot in self.index['foot']:
            self.index['foot'][foot]['freq'] += 1
            self.index['foot'][foot]['postings'].append((id, 1))
        else:
            self.index['foot'][foot] = {}
            self.index['foot'][foot]['freq'] = 1
            self.index['foot'][foot]['postings'] = [(id, 1)]

    def add_team_entity(self, team: str, id: int):
        team = team.lower()
        words = team.split()
        for w in words:
            if w in self.index['team']:
                self.index['team'][w]['freq'] += 1
                self.index['team'][w]['postings'].append((id, 1))
            else:
                self.index['team'][w] = {}
                self.index['team'][w]['freq'] = 1
                self.index['team'][w]['postings'] = [(id, 1)]

    def add_number_entity(self, number: int, id: int):
        quart = map_number_to_range(number)

        if quart in self.index['number']:
            self.index['number'][quart]['freq'] += 1
            self.index['number'][quart]['postings'].append((id, 1))
        else:
            self.index['number'][quart] = {}
            self.index['number'][quart]['freq'] = 1
            self.index['number'][quart]['postings'] = [(id, 1)]

    def add_text_entity(self, entity: dict, id: int):
        text = ""

        if 'name' in entity:
            text += entity["name"] + "\n"
        if 'position' in entity:
            text += entity["position"] + "\n"
        if 'nationality' in entity:
            text += entity["nationality"] + "\n"
        if 'foot' in entity:
            text += entity["foot"] + "\n"
        if 'team' in entity:
            text += entity["team"] + "\n"
        if 'number' in entity:
            text += str(entity["number"]) + "\n"
        if 'text' in entity:
            text += entity["text"]

        text = text.lower()
        tokens = nltk.word_tokenize(text)

        tokens = list(filter(lambda token: token.isalnum(), tokens))

        tokens.sort()
        quant = {}
        for token in tokens:
            if token in quant:
                quant[token] += 1
            else:
                quant[token] = 1

        for token in quant:
            if token in self.index['term']:
                self.index['term'][token]['freq'] += 1
                self.index['term'][token]['postings'].append((id, quant[token]))
            else:
                self.index['term'][token] = {}
                self.index['term'][token]['freq'] = 1
                self.index['term'][token]['postings'] = [(id, quant[token])]


if __name__ == '__main__':
    index = FrequencyIndex()
    index.create_from_json()
    index.save_index()

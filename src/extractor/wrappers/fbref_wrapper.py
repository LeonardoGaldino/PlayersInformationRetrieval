import bs4
import re

# SO PARA TESTE
IN_FILE = '../../../samples_pages/page-53-[fbref].html'
#IN_FILE = '../../crawler/pagesHeuristica/Fbref/page30.html'


class FbrefWrapper:

    def __init__(self):
        self.player = {}
        pass

    def extract_player_entity(self, file: str) -> dict:
        html_file = open(file, 'r')
        soup = bs4.BeautifulSoup(html_file, 'html.parser')

        player_container = soup.find("div", itemtype="https://schema.org/Person")
        self.player["name"] = player_container.find("h1").get_text()
        player_infos = player_container.find_all("p")
        player_infos_list = []

        for i in range(len(player_infos)):
            player_infos_list.append(player_infos[i].contents)

        player_infos_list = self.process_list(player_infos_list)

        if player_infos_list[0] != 'Position':
            player_infos_list.pop(0)

        if 'Position' in player_infos_list:
            self.player["position"] = player_infos_list[player_infos_list.index('Position') + 1].split(' ')[0]

        if 'Footed' in player_infos_list:
            self.player["foot"] = player_infos_list[player_infos_list.index('Footed') + 1]

        if 'Born' in player_infos_list:
            birthplace_r = player_infos_list[player_infos_list.index('Born') + 2]
            birthplace = re.search(r"^in (.*)$", birthplace_r)

            if birthplace is not None:
                country = re.search(r"^.*, ([.*, ]?.*)$", birthplace.group(1))

                if country is not None:
                    self.player["nationality"] = country.group(1)
                else:
                    self.player["nationality"] = birthplace.group(1)

        if 'Club' in player_infos_list:
            self.player["team"] = player_infos_list[player_infos_list.index('Club') + 1].replace('(', '')

        url = file.split("/")[-1].replace("page-", "").replace("_", "/")
        self.player["url"] = url

        return self.player

    @staticmethod
    def process_list(li: list) -> list:
        temp_list = []

        for i in li:
            if isinstance(i, list):
                for j in i:
                    temp_list.append(j)
            else:
                temp_list.append(i)

        for i in range(len(temp_list)):
            if isinstance(temp_list[i], bs4.Tag):
                temp_list[i] = temp_list[i].get_text()
            temp_list[i] = re.sub(r"^\W+|\W+$|[\xa0\n]|(?<=\d\d),", '', temp_list[i])

        temp_list = [x for x in temp_list if x != '']

        return temp_list

    @staticmethod
    def month_to_int(month: str) -> int:
        months = {
            'January': 1,
            'February': 2,
            'March': 3,
            'April': 4,
            'May': 5,
            'June': 6,
            'July': 7,
            'August': 8,
            'September': 9,
            'October': 10,
            'November': 11,
            'December': 12
        }

        return months.get(month)

# SO PARA TESTE
def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))


if __name__ == '__main__':
    wrapper = FbrefWrapper()
    dicionary = wrapper.extract_player_entity(IN_FILE)
    pretty(dicionary)

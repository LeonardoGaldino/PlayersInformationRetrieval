import bs4
import re

# SO PARA TESTE
IN_FILE = '../../../samples_pages/page-18-[soccerway].html'


class SoccerWayWrapper:

    def __init__(self):
        self.player = {}
        pass

    def extract_player_entity(self, file: str) -> dict:
        html_file = open(file, 'r')
        soup = bs4.BeautifulSoup(html_file, 'html.parser')

        player_container = soup.find("div", class_="content").find("dl")
        player_infos = player_container.find_all(["dt", "dd"])

        player_infos_list = []
        for i in range(len(player_infos)):
            player_infos_list.append(player_infos[i].get_text())

        self.player["name"] = {}

        if 'First name' in player_infos_list:
            self.player["name"] = player_infos_list[player_infos_list.index('First name') + 1]
            if 'Last name' in player_infos_list:
                self.player["name"] += ' ' + player_infos_list[player_infos_list.index('Last name') + 1]

        if 'Nationality' in player_infos_list:
            self.player["nationality"] = player_infos_list[player_infos_list.index('Nationality') + 1]

        if 'Position' in player_infos_list:
            self.player["position"] = player_infos_list[player_infos_list.index('Position') + 1]

        if 'Foot' in player_infos_list:
            self.player["foot"] = player_infos_list[player_infos_list.index('Foot') + 1]

        return self.player

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
    wrapper = SoccerWayWrapper()
    dicionary = wrapper.extract_player_entity(IN_FILE)
    pretty(dicionary)

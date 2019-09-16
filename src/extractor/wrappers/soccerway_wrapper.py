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
        self.player["date_of_birth"] = {}
        self.player["birthplace"] = {}

        if 'First name' in player_infos_list:
            self.player["name"]["first_name"] = player_infos_list[player_infos_list.index('First name') + 1]

        if 'Last name' in player_infos_list:
            self.player["name"]["last_name"] = player_infos_list[player_infos_list.index('Last name') + 1]

        if 'Nationality' in player_infos_list:
            self.player["nationality"] = player_infos_list[player_infos_list.index('Nationality') + 1]

        if 'Date of birth' in player_infos_list:
            date = player_infos_list[player_infos_list.index('Date of birth') + 1]
            date_infos = re.split(' ', date)

            self.player["date_of_birth"]["day"] = int(date_infos[0])
            self.player["date_of_birth"]["month"] = self.month_to_int(date_infos[1])
            self.player["date_of_birth"]["year"] = int(date_infos[2])

        if 'Age' in player_infos_list:
            self.player["age"] = player_infos_list[player_infos_list.index('Age') + 1]

        if 'Country of birth' in player_infos_list:
            self.player["birthplace"]["country"] = player_infos_list[player_infos_list.index('Country of birth') + 1]

        if 'Place of birth' in player_infos_list:
            self.player["birthplace"]["city"] = player_infos_list[player_infos_list.index('Place of birth') + 1]

        if 'Position' in player_infos_list:
            self.player["position"] = player_infos_list[player_infos_list.index('Position') + 1]

        if 'Height' in player_infos_list:
            self.player["height"] = player_infos_list[player_infos_list.index('Height') + 1]

        if 'Weight' in player_infos_list:
            self.player["weight"] = player_infos_list[player_infos_list.index('Weight') + 1]

        if 'Foot' in player_infos_list:
            self.player["foot"] = player_infos_list[player_infos_list.index('Foot') + 1]

        # SO PARA TESTE
        self.pretty(self.player)

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
    def pretty(self, d, indent=0):
        for key, value in d.items():
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                self.pretty(value, indent+1)
            else:
                print('\t' * (indent+1) + str(value))


if __name__ == '__main__':
    wrapper = SoccerWayWrapper()
    wrapper.extract_player_entity(IN_FILE)

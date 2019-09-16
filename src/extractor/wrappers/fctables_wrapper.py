import bs4
import re

# SO PARA TESTE
IN_FILE = '../../../samples_pages/page-21-[fctables].html'


class FCTablesWrapper:

    def __init__(self):
        self.player = {}
        pass

    def extract_player_entity(self, file: str) -> dict:
        html_file = open(file, 'r')
        soup = bs4.BeautifulSoup(html_file, 'html.parser')

        player_container = soup.find_all("div", class_="panel-body")[6]\
            .find("div", class_="col-lg-10 col-md-9 col-xs-12")

        player_infos = player_container.select('div.col-xs-8, label.col-xs-4')
        player_infos_list = []

        for i in range(len(player_infos)):
            player_infos_list.append(player_infos[i].get_text())

        if 'Name:' in player_infos_list:
            self.player["name"] = player_infos_list[player_infos_list.index('Name:') + 1]

        if 'Team:' in player_infos_list:
            self.player["team"] = player_infos_list[player_infos_list.index('Team:') + 1]

        if 'Number:' in player_infos_list:
            self.player["number"] = player_infos_list[player_infos_list.index('Number:') + 1]

        if 'Position:' in player_infos_list:
            self.player["position"] = player_infos_list[player_infos_list.index('Position:') + 1]

        if 'Height:' in player_infos_list:
            self.player["height"] = player_infos_list[player_infos_list.index('Height:') + 1]

        if 'Weight:' in player_infos_list:
            self.player["weight"] = player_infos_list[player_infos_list.index('Weight:') + 1]

        if 'Date of birth:' in player_infos_list:
            birth_info = player_infos_list[player_infos_list.index('Date of birth:') + 1]
            age = re.match(r"^\d\d", birth_info)

            self.player["age"] = int(age[0])

            birth_info_list = re.match(r".*\((.*)\)", birth_info).group(1).split('-')
            self.player["date_of_birth"] = {}

            self.player["date_of_birth"]["day"] = int(birth_info_list[2])
            self.player["date_of_birth"]["month"] = int(birth_info_list[1])
            self.player["date_of_birth"]["year"] = int(birth_info_list[0])

        if 'Nationality:' in player_infos_list:
            self.player["nationality"] = player_infos_list[player_infos_list.index('Nationality:') + 1]

        # SO PARA TESTE
        self.pretty(self.player)

        return self.player

    # SO PARA TESTE
    def pretty(self, d, indent=0):
        for key, value in d.items():
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                self.pretty(value, indent+1)
            else:
                print('\t' * (indent+1) + str(value))


if __name__ == '__main__':
    wrapper = FCTablesWrapper()
    wrapper.extract_player_entity(IN_FILE)

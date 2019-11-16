import bs4
import re

# SO PARA TESTE
IN_FILE = '../../../samples_pages/page-29-[fctables].html'


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
            team_list = player_infos_list[player_infos_list.index('Team:') + 1].split()
            team_list.pop()
            team = ''
            for i in range(len(team_list)):
                team += team_list[i]
                if i != len(team_list) - 1:
                    team += " "
            self.player["team"] = team

        if 'Number:' in player_infos_list:
            self.player["number"] = int(player_infos_list[player_infos_list.index('Number:') + 1])

        if 'Position:' in player_infos_list:
            self.player["position"] = player_infos_list[player_infos_list.index('Position:') + 1]

        if 'Nationality:' in player_infos_list:
            self.player["nationality"] = player_infos_list[player_infos_list.index('Nationality:') + 1][1:]

        player_text = soup.find_all("div", class_="panel-body")[8].get_text()
        if player_text:
            self.player["text"] = player_text

        url = file.split("/")[-1].replace("page-", "").replace("_", "/").replace(".html", "")
        error_s = url[:len(url)-1].rfind("/")
        if "players" != url[error_s-7:error_s]:
            url = url[:error_s] + '_' + url[error_s+1:]
        self.player["url"] = url

        return self.player

# SO PARA TESTE
def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))


if __name__ == '__main__':
    wrapper = FCTablesWrapper()
    dicionary = wrapper.extract_player_entity(IN_FILE)
    pretty(dicionary)

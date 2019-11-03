import bs4
import re

# SO PARA TESTE
#IN_FILE = '../../../samples_pages/page-70-[uefa].html'
IN_FILE = "../../crawler/pagesHeuristica/UEFA/page352.html"


class UefaWrapper:

    def __init__(self):
        self.player = {}
        pass

    def extract_player_entity(self, file: str) -> dict:
        html_file = open(file, 'r')
        soup = bs4.BeautifulSoup(html_file, 'html.parser')

        player_container = soup.find("div", class_="content-wrap")
        player_infos = player_container.find("div", class_="player-header_info")

        name = player_infos.find("h1", class_="player-header_name")
        position = player_infos.find("div", class_="player-header_category")
        nationality = player_infos.find("div", class_="player-header_country")
        team = player_infos.find("div", class_="player-header_team").find("span", class_="club-logo")

        if name is not None:
            self.player["name"] = name.get_text()

        if position is not None:
            self.player["position"] = position.get_text()

        if nationality is not None:
            self.player["nationality"] = nationality.get_text()

        if team is not None:
            self.player["team"] = team['title']

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
    wrapper = UefaWrapper()
    dicionary = wrapper.extract_player_entity(IN_FILE)
    pretty(dicionary)

import bs4
import re

# SO PARA TESTE
IN_FILE = '../../../samples_pages/page-9-[mlssoccer].html'


class MLSSoccerWrapper:

    def __init__(self):
        self.player = {}
        pass

    def extract_player_entity(self, file: str) -> dict:
        html_file = open(file, 'r')
        soup = bs4.BeautifulSoup(html_file, 'html.parser')

        player_container = soup.find('div', class_='player_container')

        title_overlay = player_container.find('div', class_='title_overlay')
        self.player["name"] = title_overlay.find('div', class_='title').get_text()
        self.player["team"] = title_overlay.find('a').get_text()
        self.player["position"] = title_overlay.find('span', class_='position').get_text()
        self.player["number"] = int(title_overlay.find('span', class_='subtitle').get_text())

        player_metas = player_container.find_all('div', class_='player_meta')

        birthplace = player_metas[1].find('div', class_='hometown').get_text().split('\n')[1].split(', ')
        self.player["nationality"] = {}
        country = "USA" if len(birthplace[1]) <= 2 else birthplace[1]
        self.player["nationality"] = country

        player_text = soup.find('div', class_="bio")
        if player_text is not None:
            self.player["text"] = player_text.get_text()

        url = file.split("/")[-1].replace("page-", "").replace("_", "/").replace(".html", "")
        self.player["url"] = url

        return self.player


# SO PARA TESTE
def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


if __name__ == '__main__':
    wrapper = MLSSoccerWrapper()
    dicionary = wrapper.extract_player_entity(IN_FILE)
    pretty(dicionary)

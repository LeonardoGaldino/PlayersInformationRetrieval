import bs4
import re

# SO PARA TESTE
IN_FILE = '../../../samples_pages/page-31-[fifa].html'


class FifaWrapper:

    def __init__(self):
        self.player = {}
        pass

    def extract_player_entity(self, file: str) -> dict:
        html_file = open(file, 'r')
        soup = bs4.BeautifulSoup(html_file, 'html.parser')

        player_container = soup.find("div", class_="fi-p--profile")

        player_num = player_container.find('span', class_="fi-p__num")
        self.player["number"] = int(player_num.get_text())

        player_infos = player_container.find('div', class_="fi-p__wrapper-text").find_all("div")

        self.player["name"] = re.search(r"(\w+[ \w+]*)", player_infos[0].get_text()).group()
        self.player["nationality"] = re.search(r"(\w+[ \w+]*)", player_infos[1].get_text()).group()
        self.player["position"] = re.search(r"(\w+[ \w+]*)", player_infos[2].get_text()).group()

        player_text = soup.find_all("div", class_="fi-p__profile-text")[1].get_text()

        if player_text is not None:
            self.player["text"] = player_text

        url = file.split("/")[-1].replace("page-", "").replace("_", "/").replace(".html", "")
        self.player["url"] = url

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
    wrapper = FifaWrapper()
    dicionary = wrapper.extract_player_entity(IN_FILE)
    pretty(dicionary)

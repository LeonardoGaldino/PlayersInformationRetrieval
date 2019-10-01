import bs4
import re

# SO PARA TESTE
IN_FILE = '../../../samples_pages/page-42-[eurosport].html'


class EurosportWrapper:

    def __init__(self):
        self.player = {}
        pass

    def extract_player_entity(self, file: str) -> dict:
        html_file = open(file, 'r')
        soup = bs4.BeautifulSoup(html_file, 'html.parser')

        player_container = soup.find("div", class_="person-head__content")

        self.player["name"] = player_container.find("h1", class_="person-head__person-name").get_text()
        self.player["position"] = player_container.find("div", class_="person-head__person-position").get_text()

        player_infos = player_container.find("ul", class_="person-info__list").find_all("div")
        player_infos_list = []

        for tag in player_infos:
            player_infos_list.append(tag.get_text().replace('\xa0', " "))

        if 'Country:' in player_infos_list:
            self.player["nationality"] = player_infos_list[player_infos_list.index('Country:') + 1]

        if 'Age:' in player_infos_list:
            self.player["age"] = re.search(r"\d+", player_infos_list[player_infos_list.index('Age:') + 1]).group()

        if 'Place of birth:' in player_infos_list:
            self.player["place_of_birth"] = player_infos_list[player_infos_list.index('Place of birth:') + 1]

        if 'Height:' in player_infos_list:
            self.player["height"] = re.search(r"\d+\.\d+", player_infos_list[player_infos_list.index('Height:') + 1]).group()

        if 'Weight:' in player_infos_list:
            self.player["weight"] = int(re.search(r"\d+", player_infos_list[player_infos_list.index('Weight:') + 1]).group())

        if "Date of birth:" in player_infos_list:
            birth_info = re.split(r"\ ", player_infos_list[player_infos_list.index('Date of birth:') + 1])

            self.player["date_of_birth"] = {}
            self.player["date_of_birth"]["day"] = int(birth_info[0])
            self.player["date_of_birth"]["month"] = self.month_to_int(birth_info[1])
            self.player["date_of_birth"]["year"] = int(birth_info[2])

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
    wrapper = EurosportWrapper()
    wrapper.extract_player_entity(IN_FILE)

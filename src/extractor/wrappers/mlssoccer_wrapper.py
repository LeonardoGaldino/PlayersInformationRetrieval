import bs4
import re

# SO PARA TESTE
IN_FILE = '../../../samples_pages/page-8-[mlssoccer].html'


def extract_player_entity(file: str) -> dict:
    player = {}
    html_file = open(file, 'r')
    soup = bs4.BeautifulSoup(html_file, 'html.parser')

    player_container = soup.find('div', class_='player_container')

    title_overlay = player_container.find('div', class_='title_overlay')
    player["name"] = title_overlay.find('div', class_='title').get_text()
    player["team"] = title_overlay.find('a').get_text()
    player["position"] = title_overlay.find('span', class_='position').get_text()
    player["number"] = int(title_overlay.find('span', class_='subtitle').get_text())

    player_metas = player_container.find_all('div', class_='player_meta')
    player["real_name"] = player_metas[0].find('div', class_='name').get_text().replace('Real Name:\n', '')

    birth_infos = player_metas[1].find('div', class_='age').get_text().split()
    player["age"] = birth_infos[1]
    birthday = re.findall(r"(\d+)", birth_infos[2], flags=re.ASCII)
    player["date_of_birth"] = {}
    player["date_of_birth"]["day"] = birthday[1]
    player["date_of_birth"]["month"] = birthday[0]
    player["date_of_birth"]["year"] = birthday[2]

    birthplace = player_metas[1].find('div', class_='hometown').get_text().split('\n')[1].split(', ')
    player["birthplace"] = {}
    player["birthplace"]["city"] = birthplace[0]
    player["birthplace"]["country"] = "USA" if len(birthplace[1]) <= 2 else birthplace[1]

    stats = player_metas[0].find_all('span', class_='stat')
    player["height"] = stats[0].get_text()
    player["weight"] = stats[1].get_text() + "lb"

    career_years = player_container.parent.find('tbody').find_all('td', attrs={"data-title": "Year"})
    career_clubs = player_container.parent.find('tbody').find_all('td', attrs={"data-title": "Club"})
    player["career"] = [{"year": career_years[i].get_text(), "club": career_clubs[i].get_text()} for i in range(len(career_years))]
    player["career"].pop()

    # SO PARA TESTE
    pretty(player)

    return player

# SO PARA TESTE
def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))


if __name__ == '__main__':
    extract_player_entity(IN_FILE)

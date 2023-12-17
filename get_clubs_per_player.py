import sys
import requests
from bs4 import BeautifulSoup

def get_clubs(player_name):
    base_url = "https://www.transfermarkt.de"
    search_url = base_url + "/schnellsuche/ergebnis/schnellsuche"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': search_url,
    }

    params = {
        'query': player_name
    }

    response = requests.get(search_url, headers=headers, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the link to the player's profile
    player_link = soup.find('table', class_='inline-table').find('tr').find_all('td')[1].find('a')['href']
    player_link = player_link.replace('profil', 'leistungsdatendetails')

    if player_link is None:
        return None
    
    player_url = base_url + player_link
    response = requests.get(player_url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    header_h1_ele = soup.find('h1')
    first_name = header_h1_ele.span.next_sibling.strip()
    last_name = header_h1_ele.find('strong').text.strip()
    clear_player_name = first_name + " " + last_name
    print(f"Name: {clear_player_name}")

    # Find the table with club history
    table = soup.find('table', class_='items').find('tbody')
    if table is not None:
        clubs = set()
        rows = table.find_all('tr')
        
        # Skip the table header row
        for row in rows:
            try:
                td = row.find_all('td')
            except IndexError:
                continue
            except TypeError:
                continue
            
            club = row.find_all('td')[3].find('a')['title']
            clubs.add(club)
        return clear_player_name, clubs


def main():
    # Beispielaufruf
    if len(sys.argv) > 1:
        player_name = sys.argv[1]
    else:
        player_name = "Lionel Messi"
    clear_player_name, clubs = get_clubs(player_name)

    if clubs is not None:
        print(f"Vereine von {clear_player_name}:")
        for club in clubs:
            print(club)
    else:
        print(f"Keine Informationen gefunden für {player_name}.")

if __name__ == "__main__":
    main()
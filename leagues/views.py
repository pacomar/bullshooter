from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

from leagues import utils

headers = {
    'authority': 'www.bullshooter.eu',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'es,en;q=0.9,en-GB;q=0.8',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://www.bullshooter.eu/',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

# Define la vista que realizará el web leagues
def leagues_view(request):
    url = 'https://www.bullshooter.eu/current-league/'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    leagues = []
    leagues_html = soup.find_all("div", class_="elementor-widget-wrap elementor-element-populated")
    leagues_html = leagues_html[2:]
    for league in leagues_html:
        image = league.find_all('img')[0].get('src')
        url = league.find_all('a')[0].get('href')
        id = url.split('/')[-2]
        name = id.replace('-', ' ').title()
        leagues.append({
            'id': id,
            'name': name,
            'url': url,
            'image': image
        })

    return render(request, "leagues.html", {"leagues": leagues})


def league_view(request, id):
    url = f'https://www.bullshooter.eu/{id}/'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    groups = []
    groups_html = soup.find_all("div", class_="elementor-tab-title")
    for i, group in enumerate(groups_html):
        name = group.find_all('a')[0].text
        groups.append({
            'index': i,
            'name': name
        })
    tables = soup.find_all("table")
    encabezados = []
    for i, table in enumerate(tables):
        [encabezados, group] = utils.parsear_tabla_html(table)
        groups[i]['table'] = group
    elementos_p = soup.find_all('p')
    hrefs = []
    for elemento_p in elementos_p:
        href = elemento_p.find('a')
        if href != None: hrefs.append(href)
    for i, href in enumerate(hrefs):
        responseScore = requests.get(href.get('href'))
        soupScore = BeautifulSoup(responseScore.content, "html.parser")
        plain_text = soupScore.find('pre').get_text()
        lineas = plain_text.split('\n')
        teamRanking = []
        playerCricketRanking = []
        player501Ranking = []

        count = 1
        for linea in lineas[(utils.find_index(lineas, 'Team Standings, sorted by Match Wins')+4):(utils.find_index(lineas, 'Last Match Results')-2)]:
            data = linea.split('|')
            teamRanking.append({
                'index': count,
                'team': data[0].strip(),
                'win_rate': data[1].strip(),
                'matches': data[2].strip(),
                'wins': data[3].strip()
            })
            count += 1

        count = 1
        for linea in lineas[(utils.find_index(lineas, 'All Cricket games, sorted by MPR:')+4):(utils.find_index(lineas, 'All X01 games, sorted by PPD:')-2)]:
            if '----' in linea: continue
            if 'Player' in linea: continue
            data = linea.split('|')
            playerCricketRanking.append({
                'index': count,
                'player': data[0].strip(),
                'team': data[1].strip(),
                'MPR': data[2].strip(),
                'Games': data[3].strip(),
                'Wins': data[4].strip(),
                'Assists': data[5].strip(),
                'Hats': data[6].strip(),
                'WHorse': data[7].strip(),
                '5MR': data[8].strip(),
                '6MR': data[9].strip(),
                '7MR': data[10].strip(),
                '8MR': data[11].strip(),
                '9MR': data[12].strip()
            })
            count += 1

        count = 1
        for linea in lineas[(utils.find_index(lineas, 'All X01 games, sorted by PPD:')+4):-2]:
            if '----' in linea: continue
            if 'Player' in linea: continue
            data = linea.split('|')
            player501Ranking.append({
                'index': count,
                'player': data[0].strip(),
                'team': data[1].strip(),
                'PPD': data[2].strip(),
                'Games': data[3].strip(),
                'Wins': data[4].strip(),
                'Hats': data[5].strip(),
                '3BD': data[6].strip(),
                'Ton80': data[7].strip(),
                'HTon': data[8].strip(),
                'LTon': data[9].strip(),
                '6DO': data[10].strip(),
                '7DO': data[11].strip(),
                '8DO': data[12].strip(),
                '9DO': data[13].strip()
            })
            count += 1
        groups[i]['teamRanking'] = teamRanking
        groups[i]['playerCricketRanking'] = playerCricketRanking
        groups[i]['player501Ranking'] = player501Ranking

    return render(request, "league.html", {"groups": groups, "encabezados": encabezados, "id": id, "league": id.replace('-', ' ').title()})
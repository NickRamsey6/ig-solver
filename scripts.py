import numpy as np
import pandas as pd
import bs4
import requests
import sys

def query_br(team1, team2):
    url = 'https://www.baseball-reference.com/friv/players-who-played-for-multiple-teams-franchises.fcgi?level=franch&t1={}&t2={}&t3=--&t4=--&utm_campaign=2023_07_ig_possible_answers&utm_source=ig&utm_medium=sr_xsite'
    url = url.format(team1, team2)
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    tables = [element.text for element in soup.find_all('tbody')]

    print(tables)

print('Enter Team1 Abbr:')
team1 = input()
print('Enter Team2 Abbr:')
team2 = input()

if __name__ == '__main__':
    query_br(team1=team1, team2=team2)
import pandas as pd


def query_br(team1, team2):
    teams_dict = {
        'ANA':'Los Angeles Angels of Anaheim',
        'ARI':'Arizona Diamondbacks',
        'ATL':'Atlanta Braves',
        'BAL':'Baltimore Orioles',
        'BOS':'Boston Red Sox',
        'CHC':'Chicago Cubs',
        'CHW':'Chicago White Sox',
        'CIN':'Cincinnati Reds',
        'CLE':'Cleveland Guardians',
        'COL':'Colorado Rockies',
        'DET':'Detroit Tigers',
        'FLA':'Florida Marlins',
        'HOU':'Houston Astros',
        'KCR':'Kansas City Royals',
        'LAD':'Los Angeles Dodgers',
        'MIL':'Milwaukee Brewers',
        'MIN':'Minnesota Twins',
        'NYM':'New York Mets',
        'NYY':'New York Yankees',
        'OAK':'Oakland Athletics',
        'PHI':'Philadelphia Phillies',
        'PIT':'Pittsburgh Pirates',
        'SDP':'San Diego Padres',
        'SEA':'Seattle Mariners',
        'SFG':'San Francisco Giants',
        'STL':'St. Louis Cardinals',
        'TBD':'Tampa Bay Rays',
        'TEX':'Texas Rangers',
        'TOR':'Toronto Blue Jays',
        'WSN':'Washington Nationals'
    }
    url = 'https://www.baseball-reference.com/friv/players-who-played-for-multiple-teams-franchises.fcgi?level=franch&t1={}&t2={}&t3=--&t4=--&utm_campaign=2023_07_ig_possible_answers&utm_source=ig&utm_medium=sr_xsite'
    url = url.format(team1, team2)
    tables = pd.read_html(url)
    batting_table = tables[0]
    pitching_table = tables[1]

    # Sort batting table by sum of games played for each team
    batting_table['sum'] = batting_table[(teams_dict[team1], 'G')] + batting_table[(teams_dict[team2], 'G')]
    sorted_batting = batting_table.sort_values([('sum', '')], ascending=True)
    rarest_batter ={
        'Name':sorted_batting[('Unnamed: 0_level_0', 'Name')].iloc[0],
        'Games':sorted_batting[('sum', '')].iloc[0]
    }

    # Sort pitching table by sum of games played for each team
    pitching_table['sum'] = pitching_table[(teams_dict[team1], 'G')] + pitching_table[(teams_dict[team2], 'G')]
    sorted_pitching = pitching_table.sort_values([('sum', '')], ascending=True)
    rarest_pitcher ={
        'Name':sorted_pitching[('Unnamed: 0_level_0', 'Name')].iloc[0],
        'Games':sorted_pitching[('sum', '')].iloc[0]
    }

    if rarest_batter['Games'] > rarest_pitcher['Games']:
        answer = rarest_pitcher['Name']
    else:
        answer=rarest_batter['Name']

    print(answer)                                
    return None

print('Enter Team1 Abbr:')
team1 = input()
print('Enter Team2 Abbr:')
team2 = input()

if __name__ == '__main__':
    query_br(team1=team1, team2=team2)
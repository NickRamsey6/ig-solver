import pandas as pd
import requests
from random import randrange

def gg_query(team1):
    # Compile a dataframe of all gold glove winners (columns: Year, Player, Team, Position)
    url = 'https://www.mlb.com/awards/gold-glove'
    r = requests.get(url)
    tables = pd.read_html(r.text)
    total_gg_df = pd.concat(tables)
    # Drop any multi year winners
    total_gg_df.drop_duplicates(subset='Player',inplace=True, keep=False)
    # Filter dataframe by team
    filt_gg_df = total_gg_df[total_gg_df['Team'] == team1]
    # Pick random player from dataframe
    filt_gg_df.reset_index(inplace=True, drop=True)
    random_player_index = randrange(len(filt_gg_df))
    gg_answer = filt_gg_df['Player'].iloc[random_player_index]
    print(gg_answer)


def query_br(team1, team2):
    # Dictionary of all active MLB teams
    teams_dict = {
        'ANA':'Los Angeles Angels',
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
        'FLA':'Miami Marlins',
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
    
    # Pass the user inputted teams into the baseball reference search query and read results into pandas dataframe
    url = 'https://www.baseball-reference.com/friv/players-who-played-for-multiple-teams-franchises.fcgi?level=franch&t1={}&t2={}&t3=--&t4=--&utm_campaign=2023_07_ig_possible_answers&utm_source=ig&utm_medium=sr_xsite'
    url = url.format(team1, team2)
    tables = pd.read_html(url)
    batting_table = tables[0]
    pitching_table = tables[1]

    # Sort batting table by sum of games played for each team
    batting_table[('Both', 'G')] = batting_table[(teams_dict[team1], 'G')] + batting_table[(teams_dict[team2], 'G')]
    sorted_batting = batting_table.sort_values([('Both', 'G')], ascending=True)
    rarest_batter ={
        'Name':sorted_batting[('Unnamed: 0_level_0', 'Name')].iloc[0],
        'Games':sorted_batting[('Both', 'G')].iloc[0]
    }

    # Sort pitching table by sum of games played for each team
    pitching_table[('Both', 'G')] = pitching_table[(teams_dict[team1], 'G')] + pitching_table[(teams_dict[team2], 'G')]
    sorted_pitching = pitching_table.sort_values([(('Both', 'G'))], ascending=True)
    rarest_pitcher ={
        'Name':sorted_pitching[('Unnamed: 0_level_0', 'Name')].iloc[0],
        'Games':sorted_pitching[(('Both', 'G'))].iloc[0]
    }

    # Both table
    # both_df = pd.merge(left=batting_table, right=pitching_table, left_on=(('Unnamed: 0_level_0', 'Name')), right_on=(('Unnamed: 0_level_0', 'Name')))
    #print(both_df)
    # TODO - check if pitcher is actually a position player?

    if rarest_batter['Games'] > rarest_pitcher['Games']:
        answer = rarest_pitcher['Name']
    else:
        answer=rarest_batter['Name']

    print(answer)

    # print(sorted_batting[('Unnamed: 0_level_0', 'Name')].eq(answer).any())                     
    return None

# TODO validate user inputs with team dict
# Collect user inputs from command line
print('Enter Team1 Abbr:')
team1 = input()
print('Enter Team2 Abbr:')
team2 = input()

if __name__ == '__main__':
    query_br(team1=team1, team2=team2)
    gg_query(team1=team1)
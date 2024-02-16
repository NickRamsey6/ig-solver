import pandas as pd
import requests
from random import randrange

team_dict={
    'ANA':{
        'name':'Los Angeles Angels',
        'award':['LA Angels', 'Anaheim', 'California'],
        'league':'American'
    },
    'ARI':{
        'name':'Arizona Diamondbacks',
        'award':['Arizona'],
        'league':'National'
    },
    'ATL':{
        'name':'Atlanta Braves',
        'award':['Atlanta'],
        'league':'National'
    },
    'BAL':{
        'name':'Baltimore Orioles',
        'award':['Baltimore'],
        'league':'American'
    },
    'BOS':{
        'name':'Boston Red Sox',
        'award':['Boston'],
        'league':'American'
    },
    'CHC':{
        'name':'Chicago Cubs',
        'award':['Chicago', 'Chi Cubs'],
        'league':'National'
    },
    'CHW':{
        'name':'Chicago White Sox',
        'award':['Chicago', 'Chi White Sox'],
        'league':'American'
    },
    'CIN':{
        'name':'Cincinnati Reds',
        'award':['Cincinnati'],
        'league':'National'
    },
    'CLE':{
        'name':'Cleveland Guardians',
        'award':['Cleveland'],
        'league':'American'
    },
    'COL':{
        'name':'Colorado Rockies',
        'award':['Colorado'],
        'league':'National'
    },
    'DET':{
        'name':'Detroit Tigers',
        'award':['Detroit'],
        'league':'American'
    },
    'FLA':{
        'name':'Miami Marlins',
        'award':['Florida'],
        'league':'National'
    },
    'HOU':{
        'name':'Houston Astros',
        'award':['Houston'],
        'league':'Both'
    },
    'KCR':{
        'name':'Kansas City Royals',
        'award':['Kansas City'],
        'league':'American'
    },
    'LAD':{
        'name':'Los Angeles Dodgers',
        'award':['Los Angeles', 'LA Dodgers'],
        'league':'National'
    },
    'MIL':{
        'name':'Milwaukee Brewers',
        'award':['Milwaukee'],
        'league':'National'
    },
    'MIN':{
        'name':'Minnesota Twins',
        'award':['Minnesota'],
        'league':'American'
    },
    'NYM':{
        'name':'New York Mets',
        'award':['New York', 'NY Mets'],
        'league':'National'
    },
    'NYY':{
        'name':'New York Yankees',
        'award':['New York', 'NY Yankees'],
        'league':'American'
    },
    'OAK':{
        'name':'Oakland Athletics',
        'award':['Oakland'],
        'league':'American'
    },
    'PHI':{
        'name':'Philadelphia Phillies',
        'award':['Philadelphia'],
        'league':'National'
    },
    'PIT':{
        'name':'Pittsburgh Pirates',
        'award':['Pittsburgh'],
        'league':'National'
    },
    'SDP':{
        'name':'San Diego Padres',
        'award':['San Diego'],
        'league':'National'
    },
    'SEA':{
        'name':'Seattle Mariners',
        'award':['Seattle'],
        'league':'American'
    },
    'SFG':{
        'name':'San Francisco Giants',
        'award':['San Francisco'],
        'league':'National'
    },
    'STL':{
        'name':'St. Louis Cardinals',
        'award':['St. Louis'],
        'league':'National'
    },
    'TBD':{
        'name':'Tampa Bay Rays',
        'award':['Tampa Bay'],
        'league':'American'
    },
    'TEX':{
        'name':'Texas Rangers',
        'award':['Texas'],
        'league':'American'
    },
    'TOR':{
        'name':'Toronto Blue Jays',
        'award':['Toronto'],
        'league':'American'
    },
    'WSN':{
        'name':'Washington Nationals',
        'award':['Washington', 'Montreal'],
        'league':'National'
    }
}

# Set up inputs for actual columns
teams = team_dict.keys()
awards = ['GG']

print('Enter column 1')
col1 = input()
print('Enter Row 1')
row1 = input()
print('Enter Row 2')
row2 = input()
print('Enter Row 3')
row3= input()

# Validate User input - Could be refactored!! DRY!!
# while True:
#     print('Enter Team1 Abbr:')
#     team1 = input()
#     if team1 not in team_dict.keys():
#         print('Invalid Team Abbr')
#         continue
#     else:
#         break
# while True:
#     print('Enter Team2 Abbr:')
#     team2 = input()
#     if team2 not in team_dict.keys():
#         print('Invalid Team Abbr')
#         continue
#     else:
#         break

# teams = []

def gg_query(team1):
    # Compile a dataframe of all gold glove winners (columns: Year, Player, Team, Position)
    url = 'https://www.mlb.com/awards/gold-glove'
    r = requests.get(url)
    tables = pd.read_html(r.text)
    
    # Set league for each table, first table is American League, there should be one table per league per year
    i=0
    for table in tables:
        if i == 0:
            table['League'] = 'American'
        elif i % 2 == 0:
            table['League'] = 'American'
        else:
            table['League'] = 'National'
        i+=1
    total_gg_df = pd.concat(tables)
    # Edge case - Houston spent time in both leagues
    total_gg_df.loc[total_gg_df['Team'] == 'Houston', 'League'] = 'Both'

    # Drop any multi year winners
    total_gg_df.drop_duplicates(subset='Player',inplace=True, keep=False)

    # Filter by League - helps because some cities with two teams are designated by league
    filt_gg_df = total_gg_df[total_gg_df['League'] == (team_dict[team1]['league'])]

    # Filter dataframe by team
    filt_gg_df = filt_gg_df[filt_gg_df['Team'].isin(team_dict[team1]['award'])]

    # # Pick random player from dataframe
    filt_gg_df.reset_index(inplace=True, drop=True)
    random_player_index = randrange(len(filt_gg_df))
    gg_answer = filt_gg_df['Player'].iloc[random_player_index]

    print(gg_answer)


def query_br(team1, team2):
    # Pass the user inputted teams into the baseball reference search query and read results into pandas dataframe
    url = 'https://www.baseball-reference.com/friv/players-who-played-for-multiple-teams-franchises.fcgi?level=franch&t1={}&t2={}&t3=--&t4=--&utm_campaign=2023_07_ig_possible_answers&utm_source=ig&utm_medium=sr_xsite'
    url = url.format(team1, team2)
    tables = pd.read_html(url)
    batting_table = tables[0]
    pitching_table = tables[1]

    # Sort batting table by sum of games played for each team
    batting_table[('Both', 'G')] = batting_table[((team_dict[team1]['name']), 'G')] + batting_table[((team_dict[team2]['name']), 'G')]
    sorted_batting = batting_table.sort_values([('Both', 'G')], ascending=True)
    rarest_batter ={
        'Name':sorted_batting[('Unnamed: 0_level_0', 'Name')].iloc[0],
        'Games':sorted_batting[('Both', 'G')].iloc[0]
    }

    # Sort pitching table by sum of games played for each team
    pitching_table[('Both', 'G')] = pitching_table[((team_dict[team1]['name']), 'G')] + pitching_table[((team_dict[team2]['name']), 'G')]
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



if __name__ == '__main__':
    if col1 in teams:
        query_br(team1=col1, team2=row1)
        query_br(team1=col1, team2=row2)
        query_br(team1=col1, team2=row3)
    if col1 in awards:
        gg_query(team1=row1)
        gg_query(team1=row2)
        gg_query(team1=row3)
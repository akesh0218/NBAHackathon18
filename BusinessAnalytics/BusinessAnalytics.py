#This program predicts the total international views for each NBA game in the given test set 

import csv

test_set = open('test_set_PythonMentality.csv', 'rb')
test_set_reader = csv.reader(test_set)



#This function prints the number of predicted views for each game
def predict_views(game_id):
    views = 0
    wp = win_percentage(game_id) #Stores the total win percentage for participating teams
    active_all_stars = float(total_all_stars(game_id)) #Stores the number of total active all stars in each game
    team_1_marketable = marketability_team1(game_id) #True if team 1 is a marketable team, false otherwise
    team_2_marketable = marketability_team2(game_id) #True if team 2 is a marketable team, false otherwise

    #This algorithm weighs different factors that affect NBA viewership and prints out the total predicted views 
    if wp != 0:
        views = (20000 * wp) * (1.65 + (active_all_stars + .5)/10)
    else:
        views = (20000 * 0.6) * (1.65 + (active_all_stars + .5)/10)
    if team_1_marketable == True:
        views = views * 1.2
    else:
        views = views * .8
    if team_2_marketable == True:
        views = views * 1.2
    else:
        views = views * .8
    if active_all_stars >= 5:
        views += 10000
    if wp >= .75:
        views += 5000
    if active_all_stars == 0:
        views -= 4000
    elif active_all_stars >= 1:
        views += 1700
    
    print views
    
#This function calculates the total win percentage using all of the games that both teams have played thus far
def win_percentage(game_id):
    result = 0
    test_set = open('test_set_PythonMentality.csv', 'rb')
    game_data = open('game_data.csv', 'rb')
    test_set_reader = csv.reader(test_set)
    game_data_reader = csv.reader(game_data)
    team1 = ""
    team2 = ""
    team1_wins = 0
    team2_wins = 0
    team1_losses = 0
    team2_losses = 0
    for row in test_set_reader:
        if row[1] == game_id:
            team1 = row[3]
            team2 = row[4]
    for row in game_data_reader:
        if row[1] == game_id:
            if row[3] == team1:
                team1_wins = float(row[5])
                team1_losses = float(row[6])
            elif row[3] == team2:
                team2_wins = float(row[5])
                team2_losses = float(row[6]) 

    if (team1_wins + team2_wins + team1_losses + team2_losses) != 0:
        result = (team1_wins + team2_wins) / (team1_wins + team2_wins + team1_losses + team2_losses) 
    else:
        result = 0  
    test_set.close()
    game_data.close()
    return result  

#This function returns the number of total all stars in the game
def total_all_stars(game_id):
    player_data = open('player_data.csv', 'rb')
    player_data_reader = csv.reader(player_data)
    
    all_stars = 0
    for row in player_data_reader:
        if ((row[1] == game_id and (row[6] == 'East ASG' or row[6] == 'West ASG')) and row[7] == 'Active'):
            all_stars += 1

    player_data.close()
    return all_stars

#This function returns a boolean indicating whether team 1 is marketable to fans
def marketability_team1(game_id):
    marketable = False
    test_set = open('test_set_PythonMentality.csv', 'rb')
    test_set_reader = csv.reader(test_set)

    for row in test_set_reader:
        if row[1] == game_id:
            if row[3] in ['GSW', 'CLE', 'HOU', 'BOS', 'NYK', 'PHI,', 'CHI', 'LAL', 'TOR']:
                marketable = True
    test_set.close()
    return marketable

#This function returns a boolean indicating whether team 2 is marketable to fans
def marketability_team2(game_id):
    marketable = False
    test_set = open('test_set_PythonMentality.csv', 'rb')
    test_set_reader = csv.reader(test_set)

    for row in test_set_reader:
        if row[1] == game_id:
            if row[4] in ['GSW', 'CLE', 'HOU', 'BOS', 'NYK', 'PHI,', 'CHI', 'LAL', 'TOR']:
                marketable = True
    test_set.close()
    return marketable


for row in test_set_reader:
    predict_views(row[1])


test_set.close()
import random

'''
This file contains the first naive algorithm.

The algorithm consists of two phases. In the first phase, the outcome of a match is estimated. This happens in three
steps. The first step considers the achievements of both teams in the current season up to now. This is done by
comparing their rank in the table. The second step considers the team's strength in a home or away game. In order to do
so the number of games that went lost and won at home (or away) in the current season are compared against each other.
The last steps considers the results of the last three games of both teams to check if there is a run visible. The
result of each step (one of the integer values 1, 0 or -1) is taken as a hint regarding the outcome of the match. All
hints are offset and their result represents the estimated outcome of the match. It can either be positive (home team
wins), negative (guest team wins) or zero (tie).
In the second phase, the result of the match is guessed.
'''

#This function compares the table ranks of two teams
def compare_table_pos(h_rank, g_rank):
    delta = h_rank - g_rank

    if delta < -3:
        return 1
    elif delta > 3:
        return -1
    else:
        return 0

#This function compares the strengths of the teams at home or away
def compare_home_away_strengths(h_wins, h_losses, g_wins, g_losses):
    h_strength = h_wins - h_losses
    g_strength = g_wins - g_losses

    if h_strength * g_strength >= 0:
        return 0
    elif h_strength > 0:
        return 1
    else:
        return -1

#This function decodes runs from matches' end results
def decode_run(matches):
    run = 0

    for match in matches:
        goal_diff = match[0] - match[1]

        if goal_diff > 1:
            run += 2
        elif goal_diff > 0:
            run += 1
        elif goal_diff < -1:
            run -= 2
        elif goal_diff < 0:
            run -= 1

    return run

#This function compares possible runs of both teams during the last three games
# TODO: I am not quite sure if this is what I actually wanted...
def compare_runs(h_matches, g_matches):
    delta_runs = decode_run(h_matches) - decode_run(g_matches)

    if delta_runs > 0:
        return 1
    elif delta_runs < 0:
        return -1
    else:
        return 0

#This function guesses an end result for a match
def guessResult(h_matches, g_matches, outcome):
    possibleResults = {}

    if outcome == 1:
        possibleResults = {(1,0): 0.0, (2,0): 0.0, (2,1): 0.0, (3,0): 0.0, (3,1): 0.0, (3,2): 0.0}
    elif outcome == 0:
        possibleResults = {(0,0): 0.0, (1,1): 0.0, (2,2): 0.0}
    else:
        possibleResults = {(0,1): 0.0, (0,2): 0.0, (1,2): 0.0, (0,3): 0.0, (1,3): 0.0, (2,3): 0.0}

    h_shot_goals = h_matches[0][0] + h_matches[1][0] + h_matches[2][0]

    if h_shot_goals % 3 == 0:
        for result in possibleResults:
            if int(h_shot_goals) == result[0]:
                possibleResults[result] += 1
    else:
        frac_digits = h_shot_goals - int(h_shot_goals)

        for result in possibleResults:
            if int(h_shot_goals) == result[0]:
                possibleResults[result] += int(h_shot_goals) + 1 - h_shot_goals
            elif int(h_shot_goals) + 1 == result[0]:
                possibleResults[result] += h_shot_goals - int(h_shot_goals)

if __name__ == '__main__':
    #We need two teams that play against each other (Later the names of the teams are given as an input to the program.
    #For now we define them here) TODO: Change this!
    h_team = "FC Bayern"
    g_team = "Borussia Dortmund"

    #The same we do for their table rank
    h_rank = 5
    g_rank = 9

    #The same we do for home and away wins and losses
    h_wins = 1
    h_losses = 2
    g_wins = 1
    g_losses = 2

    #The same we do for the last three matches' end results ATTENTION: Results always habe to be from home or away teams
    #point of view!
    h_matches = ((0,2), (0,2), (0,2))
    g_matches = ((0,2), (0,2), (0,2))

    for i in (0,2), (0,1), (0,0), (1,0), (2,0):
        for j in (0, 2), (0, 1), (0, 0), (1, 0), (2, 0):
            for k in (0, 2), (0, 1), (0, 0), (1, 0), (2, 0):
                for l in (0, 2), (0, 1), (0, 0), (1, 0), (2, 0):
                    for m in (0, 2), (0, 1), (0, 0), (1, 0), (2, 0):
                        for n in (0, 2), (0, 1), (0, 0), (1, 0), (2, 0):
                            print((i,j,k), ",", (l,m,n), ": ", compare_runs((i,j,k), (l,m,n)))
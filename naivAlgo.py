import random

'''
This file contains the first naive algorithm.

The algorithm consists of two phases. In the first phase, the outcome of a match is estimated. This happens in three
steps. The first step considers the achievements of both teams in the current season up to now. This is done by
comparing their rank in the table. The second step considers the team's strength in a home or away game. In order to do
so the number of games that went lost and won at home (or away) in the current season are compared against each other.
(...) The result of each step (one of the integer values 1, 0 or -1) is taken as a hint regarding the outcome of the
match. All hints are offset and their result represents the estimated outcome of the match. It can either be positive
(home team wins), negative (guest team wins) or zero (tie). (...) In the second phase, the result of the match is
guessed.
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

if __name__ == '__main__':
    #We need two teams that play against each other (Later the names of the teams are given as an input to the program.
    #For now we define them here) TODO: Change this!
    h_team = "FC Bayern"
    g_team = "Borussia Dortmund"

    #The same we do for their table rank
    h_rank = 5
    g_rank = 9

    #The same we do for home and away wins and losses
    h_wins = 5
    h_losses = 4
    g_wins = 4
    g_losses = 3

    print(compare_home_away_strengths(h_wins,h_losses, g_wins, g_losses))
import random
import api_connector as api

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

    h_avg_shot_goals = (h_matches[0][0] + h_matches[1][0] + h_matches[2][0]) / 3
    h_avg_got_goals = (h_matches[0][1] + h_matches[1][1] + h_matches[2][1]) / 3
    g_avg_shot_goals = (g_matches[0][0] + g_matches[1][0] + g_matches[2][0]) / 3
    g_avg_got_goals = (g_matches[0][1] + g_matches[1][1] + g_matches[2][1]) / 3

    avg_goals = [h_avg_shot_goals, h_avg_got_goals, g_avg_shot_goals, g_avg_got_goals]#((h_avg_shot_goals, g_avg_got_goals), (h_avg_got_goals, g_avg_shot_goals))

    # if outcome == -1:
    #     avg_goals = ((h_avg_got_goals, g_avg_shot_goals), (h_avg_shot_goals, g_avg_got_goals))

    #Depending on the predicted outcome diffent results are possible
    if outcome == 0:
        possibleResults = {(0, 0): 0.0, (1, 1): 0.0, (2, 2): 0.0}

        for average in avg_goals:
            if average >= 2:
                possibleResults[(2, 2)] += 1.0
            elif average > 1:
                possibleResults[(2, 2)] += average - int(average)
                possibleResults[(1, 1)] += int(average) + 1.0 - average
            elif average == 1:
                possibleResults[(1, 1)] += 1.0
            elif average > 0:
                possibleResults[(1, 1)] += average - int(average)
                possibleResults[(0, 0)] += int(average) + 1.0 - average
            else:
                possibleResults[(0, 0)] += 1.0
    else:
        possibleResults = {(1, 0): 0.0, (2, 0): 0.0, (2, 1): 0.0, (3, 0): 0.0, (3, 1): 0.0, (3, 2): 0.0}

        if outcome == 1:
            avg_goals = [h_avg_shot_goals, g_avg_got_goals, h_avg_got_goals, g_avg_shot_goals]
        else:
            avg_goals = [h_avg_got_goals, g_avg_shot_goals, h_avg_shot_goals, g_avg_got_goals]

        for average in avg_goals[0:2]:
            if average >= 3:
                possibleResults[(3, 0)] += 1.0
                possibleResults[(3, 1)] += 1.0
                possibleResults[(3, 2)] += 1.0
            elif average > 2:
                possibleResults[(3, 0)] += average - int(average)
                possibleResults[(3, 1)] += average - int(average)
                possibleResults[(3, 2)] += average - int(average)
                possibleResults[(2, 0)] += int(average) + 1.0 - average
                possibleResults[(2, 1)] += int(average) + 1.0 - average
            elif average == 2:
                possibleResults[(2, 0)] += 1.0
                possibleResults[(2, 1)] += 1.0
            elif average > 1:
                possibleResults[(2, 0)] += average - int(average)
                possibleResults[(2, 1)] += average - int(average)
                possibleResults[(1, 0)] += int(average) + 1.0 - average
            elif average == 1:
                possibleResults[(1, 0)] += 1.0
            elif average > 0:
                possibleResults[(1, 0)] += average - int(average)
            else:
                possibleResults[(1, 0)] += 1.0

        for average in avg_goals[2:4]:
            if average >= 2:
                possibleResults[(3, 2)] += 1.0
            elif average > 1:
                possibleResults[(3, 2)] += average - int(average)
                possibleResults[(3, 1)] += int(average) + 1.0 - average
                possibleResults[(2, 1)] += int(average) + 1.0 - average
            elif average == 1:
                possibleResults[(3, 1)] += 1.0
                possibleResults[(2, 1)] += 1.0
            elif average > 0:
                possibleResults[(3, 1)] += average - int(average)
                possibleResults[(2, 1)] += average - int(average)
                possibleResults[(3, 0)] += int(average) + 1.0 - average
                possibleResults[(2, 0)] += int(average) + 1.0 - average
                possibleResults[(1, 0)] += int(average) + 1.0 - average
            else:
                possibleResults[(3, 0)] += 1.0
                possibleResults[(2, 0)] += 1.0
                possibleResults[(1, 0)] += 1.0

    #max(possibleResults.items(), )
    if outcome == 1:
        return 1
    else:
        return 2

                # for i in range(4, -1):
    #     for j in range(2):
    #         if avg_goals[0][j] > i:
    #             for res in possibleResults:
    #                 if res[0] == i and i == 3:
    #                     possibleResults[res] += 1.0
    #                 elif res[0] == i:
    #                     possibleResults[res] +=
    #                 elif res[0] == i + 1:
    #                     possibleResults
    #         elif avg_goals[0][j] == i:
    #
    # #Estimate winning teams goals
    # for goals in avg_goals[0]:
    #     if goals >= 3 and outcome != 0:
    #         possibleResults[(3,0)] += 1.0
    #         possibleResults[(3,1)] += 1.0
    #         possibleResults[(3,2)] += 1.0
    #     elif goals >= 2 and outcome == 0:
    #         possibleResults[(2, 2)] += 1.0
    #     else:
    #         if goals >= 2:
    #             possibleResults[(3,0)] += goals - int(goals)
    #             possibleResults[(3,1)] += goals - int(goals)
    #             possibleResults[(3,2)] += goals - int(goals)
    #             possibleResults[(2,0)] += int(goals) - goals + 1
    #             possibleResults[(2,1)] += int(goals) - goals + 1
    #         elif goals >= 1:
    #
    #
    #
    # if h_shot_goals % 3 == 0:
    #     for result in possibleResults:
    #         if int(h_shot_goals) == result[0]:
    #             possibleResults[result] += 1
    # else:
    #     frac_digits = h_shot_goals - int(h_shot_goals)
    #
    #     for result in possibleResults:
    #         if int(h_shot_goals) == result[0]:
    #             possibleResults[result] += int(h_shot_goals) + 1 - h_shot_goals
    #         elif int(h_shot_goals) + 1 == result[0]:
    #             possibleResults[result] += h_shot_goals - int(h_shot_goals)

if __name__ == '__main__':
    #We need two teams that play against each other (Later the names of the teams are given as an input to the program.
    #For now we define them here) TODO: Change this!
    api.init()
    h_team = "Bayern"
    g_team = "Borussia Dortmund"

    #The same we do for their table rank
    h_rank = api.get_rank(h_team)
    g_rank = api.get_rank(g_team)

    print("Ranks: ", h_rank, g_rank)
    #The same we do for home and away wins and losses
    h_wins = api.get_games_won(h_team, True)
    h_losses = 2
    g_wins = api.get_games_won(g_team, False)
    g_losses = 2

    print("Ranks: ", h_wins, h_losses, g_wins, g_losses)

    #The same we do for the last three matches' end results ATTENTION: Results always habe to be from home or away teams
    #point of view!
    h_matches = api.get_last_three_games(h_team)
    # g_matches = api.get_last_three_games(g_team)
    g_matches = ((4, 3), (3, 1), (2, 0))


    print("Matches ", h_matches, g_matches)
    result = compare_table_pos(h_rank, g_rank) + compare_home_away_strengths(h_wins, h_losses, g_wins, g_losses) + compare_runs(h_matches, g_matches)

    print("Result ", result)

import  helper, json, urllib.request
import http.client , json , sys, time, dateutil.parser
from fuzzywuzzy import fuzz


API_URL="http://api.football-data.org/v1/"
API_KEY=""

COMPETITION_ID="452" #Bundesliga 17/18
COMPETITION_ID_LAST="430" #Bundesliga 16/17

#common data:
current_league = {}
last_league = {}
teams = {}

def read_api_key():
    global API_KEY
    with open('api_key', 'r') as f:
        API_KEY = f.read()

def api_call(call):
    with urllib.request.urlopen(API_URL + call ) as url:
        return json.loads(url.read().decode())

def get_common_data():
    global current_league
    global last_league
    global teams

    current_league = api_call("competitions/" + COMPETITION_ID + "/fixtures")
    last_league = api_call("competitions/" + COMPETITION_ID_LAST + "/fixtures")
    teams= api_call("competitions/" + COMPETITION_ID + "/teams")["teams"]

def init():
    read_api_key()
    get_common_data()

#maybe we should use approximate string matching later
def get_team_id_by_name(team_name):

    best_match_id = 0;
    best_match_val = 0;
    current_id = 0;

    for team in teams:
        if len(team_name) > 3:
            current_val = fuzz.token_sort_ratio(team_name.lower(), team["name"].lower())
            # print(team["name"] +  " " + str(current_val))
        else:
            current_val = fuzz.token_sort_ratio(team_name.lower(), team["code"].lower())
            # print(team["code"] + " " + str(current_val))
        if current_val > best_match_val :
            best_match_id = current_id
            best_match_val = current_val
        current_id +=1

    team_api_name = teams[best_match_id]["name"]
    team_api_id = teams[best_match_id]["_links"]["self"]["href"].split("/")[-1]
    return team_api_name, team_api_id


def get_fixture(year):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': API_KEY, 'X-Response-Control': 'minified'}
    connection.request('GET', '/v1/teams/6/fixtures?season=' + str(year), None, headers)
    response = json.loads(connection.getresponse().read().decode())

    print(response)

def get_rank(team):
    team_name, team_id=get_team_id_by_name(team)
    # print("Look rank for: " + team_name)
    league_table = api_call("competitions/" + COMPETITION_ID + "/leagueTable")
    if( league_table["matchday"] < 4):
        #too few entries, we have to use table from the last year
        # print("LAST YEAR")
        league_table = api_call("competitions/" + COMPETITION_ID_LAST + "/leagueTable")
    position = -1
    for team in league_table["standing"]:
        if ( team["teamName"] == team_name ):
            position = team["position"]
            break
    return position
    # print("Error: team " + team_name + " not present in this league") #TODO: handle futher: show in lower league


def get_games_won(team, home_games=True):
    team_name, team_id = get_team_id_by_name(team)
    #count current games
    won_games = 0;
    finished_games =0;
    for game in current_league["fixtures"]:
        if(game["status"] == "FINISHED"):
            if(home_games):
                if(game["homeTeamName"] == team_name):
                    finished_games += 1
                    if (game["result"]["goalsHomeTeam"] > game["result"]["goalsAwayTeam"]):
                        won_games += 1
            else:
                if (game["awayTeamName"] == team_name):
                    finished_games += 1
                    if (game["result"]["goalsHomeTeam"] < game["result"]["goalsAwayTeam"]):
                        won_games += 1

    # print("Actual league played: " + str(finished_games))
    # print("Actual league won: " + str(won_games))

    if(finished_games < 3):
        # print("Too few games -> look up last league")
        won_games = 0;
        finished_games = 0;
        for game in last_league["fixtures"]:
            if (game["status"] == "FINISHED"):
                if (home_games):
                    if (game["homeTeamName"] == team_name):
                        finished_games += 1
                        if (game["result"]["goalsHomeTeam"] > game["result"]["goalsAwayTeam"]):
                            won_games += 1
                else:
                    if (game["awayTeamName"] == team_name):
                        finished_games += 1
                        if (game["result"]["goalsHomeTeam"] < game["result"]["goalsAwayTeam"]):
                            won_games += 1

        # print("Last league played: " + str(finished_games))
        # print("Last league won: " + str(won_games))
    return  won_games

def get_last_three_games(team):
    team_name, team_id = get_team_id_by_name(team)
    last_games=[{"ts":0, "a":0, "b":0},{"ts":0, "a":0, "b":0},{"ts":0, "a":0, "b":0}];
    finished_games = 0;
    for game in current_league["fixtures"]:
        if (game["status"] == "FINISHED"):
            if (game["homeTeamName"] == team_name):
                finished_games += 1
                game_ts=time.mktime(dateutil.parser.parse(game["date"]).timetuple())
                for i in range(2,-1,-1):
                    if last_games[i]["ts"] < game_ts:
                        if i == 2 :
                            last_games[i] = {"ts":game_ts, "a":game["result"]["goalsHomeTeam"], "b": game["result"]["goalsAwayTeam"]}
                        else:
                            last_games[i+1] = last_games[i]
                            last_games[i] = {"ts": game_ts, "a": game["result"]["goalsHomeTeam"],
                                             "b": game["result"]["goalsAwayTeam"]}
            elif (game["awayTeamName"] == team_name):
                finished_games += 1
                game_ts = time.mktime(dateutil.parser.parse(game["date"]).timetuple())
                for i in range(2, -1, -1):
                    if last_games[i]["ts"] < game_ts:
                        if i == 2:
                            last_games[i] = {"ts": game_ts, "a": game["result"]["goalsAwayTeam"],
                                             "b": game["result"]["goalsHomeTeam"]}
                        else:
                            last_games[i + 1] = last_games[i]
                            last_games[i] = {"ts": game_ts, "a": game["result"]["goalsAwayTeam"],
                                             "b": game["result"]["goalsHomeTeam"]}

    # print("Actual league played: " + str(last_games))


    if (finished_games < 3):
        # print("Too few games -> look up last league")
        finished_games = 0;
        last_games = [{"ts": 0, "a": 0, "b": 0}, {"ts": 0, "a": 0, "b": 0}, {"ts": 0, "a": 0, "b": 0}];
        for game in last_league["fixtures"]:
            if (game["status"] == "FINISHED"):
                if (game["homeTeamName"] == team_name):
                    finished_games += 1
                    game_ts = time.mktime(dateutil.parser.parse(game["date"]).timetuple())
                    for i in range(2, -1, -1):
                        if last_games[i]["ts"] < game_ts:
                            if i == 2:
                                last_games[i] = {"ts": game_ts, "a": game["result"]["goalsHomeTeam"],
                                                 "b": game["result"]["goalsAwayTeam"]}
                            else:
                                last_games[i + 1] = last_games[i]
                                last_games[i] = {"ts": game_ts, "a": game["result"]["goalsHomeTeam"],
                                                 "b": game["result"]["goalsAwayTeam"]}
                elif (game["awayTeamName"] == team_name):
                    finished_games += 1
                    game_ts = time.mktime(dateutil.parser.parse(game["date"]).timetuple())
                    for i in range(2, -1, -1):
                        if last_games[i]["ts"] < game_ts:
                            if i == 2:
                                last_games[i] = {"ts": game_ts, "a": game["result"]["goalsAwayTeam"],
                                                 "b": game["result"]["goalsHomeTeam"]}
                            else:
                                last_games[i + 1] = last_games[i]
                                last_games[i] = {"ts": game_ts, "a": game["result"]["goalsAwayTeam"],
                                                 "b": game["result"]["goalsHomeTeam"]}

    # print("Last league played: " + str(last_games))
    return ((last_games[0]["a"], last_games[0]["b"]),(last_games[1]["a"], last_games[1]["b"]),(last_games[2]["a"], last_games[2]["b"]))

if __name__ == '__main__':
    init()
    team=(sys.argv[1])
    print(get_rank(team))
    if(sys.argv[2].lower() == "home"):
        print(get_games_won(team, True))
    else:
        print(get_games_won(team, False))
    print(get_last_three_games(team))


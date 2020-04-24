link = {"players_boxscores": "https://stats.nba.com/players/boxscores/?Season=",
        "players_general_advanced": "https://stats.nba.com/players/advanced/?sort=GP&dir=-1&Season=Season="}


def get_link(table, season, season_type):
    if season_type == "Playoffs":
        st = ["&SeasonType=Playoffs"]
    else:
        st = ["&SeasonType=Regular%20Season"]
    fin_link = link[table] + season + st
    return fin_link

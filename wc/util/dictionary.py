link = {"players_boxscores": "https://stats.nba.com/players/boxscores/?Season=",
        "players_general_advanced": "https://stats.nba.com/players/advanced/?sort=GP&dir=-1&Season="}



def get_link(table, season, season_type):
    if season_type == "Playoffs":
        st = "&SeasonType=Playoffs"
    else:
        st = "&SeasonType=Regular%20Season"
    fin_link = link[table] + season + st
    return fin_link


def get_season_types(season_type):
    if season_type == "all":
        season_types = ["Regular", "Playoffs"]
    elif season_type == "Playoffs":
        season_types = ["Playoffs"]
    elif season_type == "Regular":
        season_types = ["Regular"]

    return season_types

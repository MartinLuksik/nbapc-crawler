link = {"players_boxscores": ["https://stats.nba.com/players/boxscores/?Season=", "&SeasonType=Regular%20Season"],
        "players_general_advanced": ["https://stats.nba.com/players/advanced/?sort=GP&dir=-1&Season=Season=", "&SeasonType=Regular%20Season"]}


def get_link(table):

    return link[table]

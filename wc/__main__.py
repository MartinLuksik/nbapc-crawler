import os
from wc.universal.crawler import *
from wc.util.dictionary import *
from wc.util.save import *
from wc.util.driver import *

table = os.environ['table']
season = os.environ['season']
season_type = os.environ['season_type']
filesystem = os.environ['filesystem']
driver_path = "/chromedriver"
#driver_path = "/home/martin/temp/chromedriver"
#table = "players_boxscores"
#season = "1996-97"
#season_type = "Regular"
#filesystem = "local"
if __name__ == '__main__':
    print("Starting crawler program: " + table + "\n Season: " + season_type + "\n Season type: " + season + "\n Filesystem: " + filesystem)
    driver = get_driver(driver_path)

    seasons = []

    if season == "all":
        link = get_link(table, "2019-2020", season_type)
        seasons = get_all_seasons(link, driver)
    else:
        seasons.append(season)

    for season in seasons:
        season_types = get_season_types(season_type)
        for season_type in season_types:
            try:
                link = get_link(table, season, season_type)
                result_df = crawl(link, driver)
                save_to(result_df, season, table, season_type, filesystem)
            except:
                (print("An exception occurred in: \n Season: " + season + "\n Season type: " + season_type))
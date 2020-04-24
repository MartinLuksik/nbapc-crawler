import os
from wc.universal.crawler import *
from wc.util.dictionary import *
from wc.util.save import *
from wc.util.driver import *

table = os.environ['table']
season = os.environ['season']
season_type = os.environ['season_type']
filesystem = os.environ['filesystem']
#driver_path = "/chromedriver"
driver_path = "/home/martin/temp/chromedriver"

if __name__ == '__main__':
    print("Starting crawler program: " + table + ". Season: " + season_type + " " + season + ". Filesystem: " + filesystem)
    driver = get_driver(driver_path)

    seasons = []

    if season == "all":
        link = get_link(table, "2019-2020", season_type)
        seasons = get_all_seasons(link, driver)
    else:
        seasons.append(season)

    for season in seasons:

        if season_type == "all":
            season_types = ["Regular", "Playoffs"]
        elif season_type == "Playoffs":
            season_types = ["Playoffs"]
        elif season_types == "Regular":
            season_types = ["Regular"]

        for season_type in season_types:
            link = get_link(table, season, season_type)
            result_df = crawl(season, link, driver)
            save_to(result_df, season, table, season_type, filesystem)

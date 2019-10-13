# Takes in environment variables that has to be passed in when starting the docker container:
# table (currently only working for "boxscores")
# season (season to be crawler)
# filesystem (file system where to store the data)
# wasbaccountname (wasb account name where to store data)
# wasbaccountkey (wasb key)

import os
import players.boxscores

table = os.environ['table']
season = os.environ['season']
filesystem = os.environ['filesystem']

def start_crawler():
    if table == "boxscores":
        print("Starting crawler program: " + table + ". Season: " + season + ". Filesystem: " + filesystem)
        players.boxscores.crawl(season, filesystem)

if __name__ == '__main__':
    start_crawler()

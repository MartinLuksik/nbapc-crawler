# This will be the initial script of the program

# Tak in two arguments:
# sys.arg[0] is the name of the file
# sys.arg[1] is the type of the crawler to be executed
# sys.arg[2] is the season to be crawled

import sys
import players.boxscores


def start_crawler():
    if sys.argv[1] == "boxscores":
        print("Starting crawler program: " + sys.argv[1] + ". Season: " + sys.argv[2] + sys.argv[3])
        players.boxscores.crawl(sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    start_crawler()


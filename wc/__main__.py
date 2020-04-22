import os
from wc.universal.crawler import crawl
from wc.util.dictionary import get_link
from wc.util.save import save_to

table = os.environ['table']
season = os.environ['season']
filesystem = os.environ['filesystem']

if __name__ == '__main__':
    print("Starting crawler program: " + table + ". Season: " + season + ". Filesystem: " + filesystem)
    link = get_link(table)
    result_df = crawl(season, table)
    save_to(result_df, season, table, filesystem)

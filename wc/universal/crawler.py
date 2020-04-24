import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import time
import random


def crawl(link, driver):

    # get page source
    driver.get(link)
    sleep_t = random.randint(45,65)
    time.sleep(sleep_t)
    driver.implicitly_wait(sleep_t)

    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")

    # get num of pages
    num_of_pages = soup.find_all('div', attrs={'class': 'stats-table-pagination__info'})
    num_of_pages = str(num_of_pages[0]).split("of ")[1].split('     ')[0]
    pages = np.arange(1, int(num_of_pages) + 1, 1)
    print("The crawler has found " + num_of_pages)

    # get columns:
    c_names = soup.find('div', attrs={'class': 'nba-stat-table__overflow'}).find('thead').find_all('th')
    columns = []
    for c in c_names:
        if "hidden" not in str(c):
            columns.append(c.get_text().strip().replace("%", "_PER").replace("+", "PLUS").replace("-", "MINUS").replace("/", "_"))
    n_col = len(columns)
    print("The crawler has found the following columns: \n" + str(columns))

    # crawl data
    df_list_values = []
    row_values = []

    for page in pages:
        print("Crawling page " + str(page) + "/" + str(num_of_pages))

        stats = soup.find('div', attrs={'class': 'nba-stat-table__overflow'}).find('tbody').find_all('td')
        for i in stats:
            if "hidden" not in str(i):
                row_values.append(i.get_text().strip())
            if len(row_values) == n_col:
                print(row_values)
                df_list_values.append(row_values)
                row_values = []

        python_button = driver.find_element_by_xpath("//a[@ class ='stats-table-pagination__next']")
        python_button.click()
        time.sleep(random.randint(3, 6))
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")

    return pd.DataFrame(df_list_values, columns=columns)


def get_all_seasons(link, driver):
    driver.get(link[0] + "2019-20" + link[1])
    sleep_t = random.randint(45, 65)
    time.sleep(sleep_t)
    driver.implicitly_wait(sleep_t)

    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")

    season_labels = soup.find('select', attrs={'class': 'ng-pristine ng-untouched ng-valid ng-not-empty'}).find_all(
        "option")
    seasons = []
    for s in season_labels:
        if s.get_text().strip() != "All Seasons":
            seasons.append(s.get_text().strip())

    return seasons

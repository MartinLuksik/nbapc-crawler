import pandas as pd
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options
import random
from xvfbwrapper import Xvfb


def crawl(season, link):
    vdisplay = Xvfb()
    vdisplay.start()

    # prepare Chrome driver
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chromedriver = "/chromedriver"
    #chromedriver = "/home/martin/temp/chromedriver"
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options)

    # get page source
    driver.get(link[0] + season + link[1])
    sleep_t = random.randint(45,65)
    time.sleep(sleep_t)
    driver.implicitly_wait(sleep_t)

    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")

    # get num of pages
    num_of_pages = soup.find_all('div', attrs={'class': 'stats-table-pagination__info'})
    num_of_pages = str(num_of_pages[0]).split("of ")[1].split('     ')[0]
    pages = np.arange(1, int(num_of_pages) + 1, 1)
    print("The crawler has found " + num_of_pages + " pages in BoxScores table.")

    # get columns:
    c_names = soup.find('div', attrs={'class': 'nba-stat-table__overflow'}).find('thead').find_all('th')
    columns = []
    for c in c_names:
        if "hidden" not in str(c):
            columns.append(c.get_text().strip().replace("%", "_PER").replace("+", "PLUS").replace("-", "MINUS").replace("/", "_"))
    n_col = len(columns)
    print("The crawler has found the following columns in the table: \n" + str(columns))

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
    vdisplay.stop()

    return pd.DataFrame(df_list_values, columns=columns)

import os
import pandas as pd
import numpy as np
from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from io import StringIO  # python3; python2: BytesIO
import boto3
from azure.storage.blob import BlockBlobService
from selenium.webdriver.chrome.options import Options
from xvfbwrapper import Xvfb
import random


def crawl(season):
        #display = Display(visible=0, size=(1920, 1200))
        #display.start()

        #vdisplay = Xvfb()
        #vdisplay.start()

        # load chromedriver and open desired webpages, wait for page to load completely including java script
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        #chrome_options.add_argument('--disable-gpu')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')

        chrome_options.add_argument('--disable-dev-shm-usage')
        chromedriver = "/home/martin/temp/chromedriver"
        #chromedriver = "/chromedriver"
        driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options)
        driver.get('https://stats.nba.com/players/advanced/?sort=GP&dir=-1&Season=' + season + '&SeasonType=Regular%20Season')
        sleep_t = random.randint(45,65)
        time.sleep(sleep_t)
        driver.implicitly_wait(sleep_t)

        # pull page source and html via beautiful soup
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")

        # get number of pages
        num_of_pages = soup.find_all('div', attrs={'class': 'stats-table-pagination__info'})
        num_of_pages = str(num_of_pages[0]).split("of ")[1].split('     ')[0]
        print("The crawler has found " + num_of_pages + " pages in Leaders table." )

        pages = np.arange(1, int(num_of_pages), 1)

        # Get Player
        Player = []
        TEAM = []
        AGE = []
        GP = []
        W = []
        L = []
        MIN = []
        OFFRTG = []
        DEFRTG = []
        NETRTG = []
        AST_PER = []
        AST_TO = []
        AST_RATIO = []
        OREB_PER = []
        DREB_PER = []
        REB_PER = []
        TO_RATIO = []
        EFG_PER = []
        TS_PER = []
        USG_PER = []
        PACE = []
        PIE = []

        for page in pages:
                print("Crawling page " + str(page) + "/" + str(num_of_pages))

                # Get stats from the table:
                stats = soup.find_all('td')
                element = 0
                playersPageCounter = 0
                for i in stats:
                        if(playersPageCounter<50):
                                if element == 0:
                                        element += 1
                                elif element == 1:
                                        Player.append(i.get_text())
                                        element += 1
                                elif element == 2:
                                        TEAM.append(i.get_text())
                                        element += 1
                                elif element == 3:
                                        AGE.append(i.get_text())
                                        element += 1
                                elif element == 4:
                                        GP.append(i.get_text())
                                        element += 1
                                elif element == 5:
                                        W.append(i.get_text())
                                        element += 1
                                elif element == 6:
                                        L.append(i.get_text())
                                        element += 1
                                elif element == 7:
                                        MIN.append(i.get_text())
                                        element += 1
                                elif element == 8:
                                        OFFRTG.append(i.get_text())
                                        element += 1
                                elif element == 9:
                                        DEFRTG.append(i.get_text())
                                        element += 1
                                elif element == 10:
                                        NETRTG.append(i.get_text())
                                        element += 1
                                elif element == 11:
                                        AST_PER.append(i.get_text())
                                        element += 1
                                elif element == 12:
                                        AST_TO.append(i.get_text())
                                        element += 1
                                elif element == 13:
                                        AST_RATIO.append(i.get_text())
                                        element += 1
                                elif element == 14:
                                        OREB_PER.append(i.get_text())
                                        element += 1
                                elif element == 15:
                                        DREB_PER.append(i.get_text())
                                        element += 1
                                elif element == 16:
                                        REB_PER.append(i.get_text())
                                        element += 1
                                elif element == 17:
                                        TO_RATIO.append(i.get_text())
                                        element += 1
                                elif element == 18:
                                        EFG_PER.append(i.get_text())
                                        element += 1
                                elif element == 19:
                                        TS_PER.append(i.get_text())
                                        element += 1
                                elif element == 20:
                                        USG_PER.append(i.get_text())
                                        element += 1
                                elif element == 21:
                                        PACE.append(i.get_text())
                                        element += 1
                                elif element == 22:
                                        PIE.append(i.get_text())
                                        element = 0
                                        playersPageCounter +=1

                python_button = driver.find_element_by_xpath("//a[@ class ='stats-table-pagination__next']")
                python_button.click()
                time.sleep(random.randint(3,8))
                html = driver.page_source
                soup = BeautifulSoup(html, features="html.parser")
        
        #vdisplay.stop()
        #display.stop()
        print(Player)
        print(TEAM)
        print(PIE)
        result = pd.DataFrame({'Player': Player, 'TEAM': TEAM, 'AGE': AGE, 'GP': GP,
                               'W': W, 'L': L, 'MIN': MIN, 'OFFRTG': OFFRTG,
                               'DEFRTG': DEFRTG, 'NETRTG': NETRTG, 'AST_PER': AST_PER, 'AST/TO': AST_TO,
                               'AST_RATIO': AST_RATIO, 'OREB_PER': OREB_PER, 'DREB_PER': DREB_PER, 'REB_PER': REB_PER, 'TO_RATIO': TO_RATIO,
                               'EFG_PER': EFG_PER, 'TS_PER': TS_PER, 'USG_PER': USG_PER, 'PACE': PACE, 'PIE': PIE})

        result = result.apply(lambda x: x.map(lambda y: str(y).lstrip('\n').rstrip('\n')))

        return result

crawl("2019-2020")
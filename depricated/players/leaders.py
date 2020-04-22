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



def crawl(season, save_destination):
        #display = Display(visible=0, size=(1920, 1200))
        #display.start()

        vdisplay = Xvfb()
        vdisplay.start()

        # load chromedriver and open desired webpages, wait for page to load completely including java script
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        #chrome_options.add_argument('--disable-gpu')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')

        chrome_options.add_argument('--disable-dev-shm-usage')
        #chromedriver = "/home/luksa24/git/nbapc/nba_crawler/chromedriver"
        chromedriver = "/chromedriver"
        driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options)
        driver.get('https://stats.nba.com/leaders/?Season=' + season + '&SeasonType=Regular%20Season')
        sleep_t = random.randint(45,65)
        time.sleep(sleep_t)
        driver.implicitly_wait(sleep_t)
        #driver.get_screenshot_as_file('/screenshots/2.png')

        # pull page source and html via beautiful soup
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")
        #print(soup)

        # get number of pages
        num_of_pages = soup.find_all('div', attrs={'class': 'stats-table-pagination__info'})
        num_of_pages = str(num_of_pages[0]).split("of ")[1].split('     ')[0]
        print("The crawler has found " + num_of_pages + " pages in Leaders table." )

        # create empty arrays for each stat, where you'll add data from each page
        # after the crawl of the last page is done, create a df from these arrays

        # create range based on the number of pages in the database(how many times you have to click 'forward'
        pages = np.arange(1, int(num_of_pages)+1, 1)
        #pages = np.arange(1, 5, 1)

        # Get Player
        order = []
        Player = []
        GP = []
        MIN = []
        PTS = []
        FGM = []
        FGA = []
        FG_PER = []
        x3PM = []
        x3PA = []
        x3P_PER = []
        FTM = []
        FTA = []
        FT_PER = []
        OREB = []
        DREB = []
        REB = []
        AST = []
        STL = []
        BLK = []
        TOV = []
        EFF = []

        for page in pages:
                print("Crawling page " + str(page) + "/" + str(num_of_pages))

                # Get stats from the table:
                stats = soup.find_all('td')
                element = 1
                playersPageCounter = 0

                for i in stats:
                        if(playersPageCounter<50):
                                if element == 1:
                                        order.append(i.get_text())
                                        element += 1
                                elif element == 2:
                                        Player.append(i.get_text())
                                        element += 1
                                elif element == 3:
                                        GP.append(i.get_text())
                                        element += 1
                                elif element == 4:
                                        MIN.append(i.get_text())
                                        element += 1
                                elif element == 5:
                                        PTS.append(i.get_text())
                                        element += 1
                                elif element == 6:
                                        FGM.append(i.get_text())
                                        element += 1
                                elif element == 7:
                                        FGA.append(i.get_text())
                                        element += 1
                                elif element == 8:
                                        FG_PER.append(i.get_text())
                                        element += 1
                                elif element == 9:
                                        x3PM.append(i.get_text())
                                        element += 1
                                elif element == 10:
                                        x3PA.append(i.get_text())
                                        element += 1
                                elif element == 11:
                                        x3P_PER.append(i.get_text())
                                        element += 1
                                elif element == 12:
                                        FTM.append(i.get_text())
                                        element += 1
                                elif element == 13:
                                        FTA.append(i.get_text())
                                        element += 1
                                elif element == 14:
                                        FT_PER.append(i.get_text())
                                        element += 1
                                elif element == 15:
                                        OREB.append(i.get_text())
                                        element += 1
                                elif element == 16:
                                        DREB.append(i.get_text())
                                        element += 1
                                elif element == 17:
                                        REB.append(i.get_text())
                                        element += 1
                                elif element == 18:
                                        AST.append(i.get_text())
                                        element += 1
                                elif element == 19:
                                        STL.append(i.get_text())
                                        element += 1
                                elif element == 20:
                                        BLK.append(i.get_text())
                                        element += 1
                                elif element == 21:
                                        TOV.append(i.get_text())
                                        element += 1
                                elif element == 22:
                                        EFF.append(i.get_text())
                                        element = 1
                                        playersPageCounter +=1

                python_button = driver.find_element_by_xpath("//a[@ class ='stats-table-pagination__next']")
                python_button.click()
                time.sleep(random.randint(3,8))
                html = driver.page_source
                soup = BeautifulSoup(html, features="html.parser")
        
        vdisplay.stop()
        #display.stop()

        result = pd.DataFrame({'Player': Player, 'GP': GP, 'MIN': MIN, 'PTS': PTS,
                               'FGM': FGM, 'FGA': FGA, 'FG_per': FG_PER, 'PM_3': x3PM,
                               'PA_3': x3PA, 'FG3_per': x3P_PER, 'FTM': FTM, 'FTA': FTA,
                               'FT_per': FT_PER, 'OREB': OREB, 'DREB': DREB, 'REB': REB, 'AST': AST,
                               'STL': STL, 'BLK': BLK, 'TOV': TOV, 'EFF': EFF})

        result = result.apply(lambda x: x.map(lambda y: str(y).lstrip('\n').rstrip('\n')))
        return result

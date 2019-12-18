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
        driver.get('https://stats.nba.com/players/boxscores/?Season=' + season + '&SeasonType=Regular%20Season')
        time.sleep(30)
        driver.implicitly_wait(30)
        #driver.get_screenshot_as_file('/screenshots/2.png')

        # pull page source and html via beautiful soup
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")
        #print(soup)

        # get number of pages
        num_of_pages = soup.find_all('div', attrs={'class': 'stats-table-pagination__info'})
        num_of_pages = str(num_of_pages[0]).split("of ")[1].split('     ')[0]
        print("The crawler has found " + num_of_pages + " in BoxScores table." )

        # create empty arrays for each stat, where you'll add data from each page
        # after the crawl of the last page is done, create a df from these arrays

        # create range based on the number of pages in the database(how many times you have to click 'forward'
        pages = np.arange(1, int(num_of_pages), 1)
        #pages = np.arange(1, 5, 1)

        # Get Player
        Player = []
        PlayersTeam = []
        Match_up = []
        Date = []
        W_L = []
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
        PF = []
        Plus_Minus = []

        for page in pages:
                print("Crawling page " + str(page) + "/" + str(num_of_pages))

                # Get stats from the table:
                stats = soup.find_all('td')[:-50]

                element = 0
                for i in stats:
                        if element == 0:
                                Player.append(i.get_text())
                                element += 1
                        elif element == 1:
                                PlayersTeam.append(i.get_text())
                                element += 1
                        elif element == 2:
                                Match_up.append(i.get_text())
                                element += 1
                        elif element == 3:
                                Date.append(i.get_text())
                                element += 1
                        elif element == 4:
                                element += 1
                        elif element == 5:
                                W_L.append(i.get_text())
                                element += 1
                        elif element == 6:
                                MIN.append(i.get_text())
                                element += 1
                        elif element == 7:
                                PTS.append(i.get_text())
                                element += 1
                        elif element == 8:
                                FGM.append(i.get_text())
                                element += 1
                        elif element == 9:
                                FGA.append(i.get_text())
                                element += 1
                        elif element == 10:
                                FG_PER.append(i.get_text())
                                element += 1
                        elif element == 11:
                                x3PM.append(i.get_text())
                                element += 1
                        elif element == 12:
                                x3PA.append(i.get_text())
                                element += 1
                        elif element == 13:
                                x3P_PER.append(i.get_text())
                                element += 1
                        elif element == 14:
                                FTM.append(i.get_text())
                                element += 1
                        elif element == 15:
                                FTA.append(i.get_text())
                                element += 1
                        elif element == 16:
                                FT_PER.append(i.get_text())
                                element += 1
                        elif element == 17:
                                OREB.append(i.get_text())
                                element += 1
                        elif element == 18:
                                DREB.append(i.get_text())
                                element += 1
                        elif element == 19:
                                REB.append(i.get_text())
                                element += 1
                        elif element == 20:
                                AST.append(i.get_text())
                                element += 1
                        elif element == 21:
                                STL.append(i.get_text())
                                element += 1
                        elif element == 22:
                                BLK.append(i.get_text())
                                element += 1
                        elif element == 23:
                                TOV.append(i.get_text())
                                element += 1
                        elif element == 24:
                                PF.append(i.get_text())
                                element += 1
                        elif element == 25:
                                Plus_Minus.append(i.get_text())
                                element = 0


                python_button = driver.find_element_by_xpath("//a[@ class ='stats-table-pagination__next']")
                python_button.click()
                time.sleep(random.randint(3,6))
                html = driver.page_source
                soup = BeautifulSoup(html, features="html.parser")
        
        vdisplay.stop()
        #display.stop()

        result = pd.DataFrame({'Player': Player, 'Team': PlayersTeam, 'MATCH_UP': Match_up,
                               'GAME_DATE': Date, 'W_L': W_L, 'MIN': MIN, 'PTS': PTS,
                               'FGM': FGM, 'FGA': FGA, 'FG_per': FG_PER, 'PM_3': x3PM,
                               'PA_3': x3PA, 'FG3_per': x3P_PER, 'FTM': FTM, 'FTA': FTA,
                               'FT_per': FT_PER, 'OREB': OREB, 'DREB': DREB, 'REB': REB, 'AST': AST,
                               'STL': STL, 'BLK': BLK, 'TOV': TOV, 'PF': PF, 'Plus_Minus': Plus_Minus})

        result['Player'] = result['Player'].map(lambda x: x.lstrip('\\n').rstrip('\\n'))
        result['Team'] = result['Team'].map(lambda x: x.lstrip('\\n').rstrip('\\n'))
        result['MATCH_UP'] = result['MATCH_UP'].map(lambda x: x.lstrip('\\n').rstrip('\\n'))
        result['GAME_DATE'] = result['GAME_DATE'].map(lambda x: x.lstrip('\\n').rstrip('\\n'))    

        if save_destination == "local":
                result.to_csv('/wc/data/boxscores_' + season + '.csv', index=False, sep=';')
                print('CSV was successfully saved to /wc/data/boxscores_' + season + '.csv')
        elif save_destination == "s3":
                s3bucket = os.environ['s3bucket']
                csv_buffer = StringIO()
                result.to_csv(csv_buffer, index=False, sep=';')
                s3 = boto3.resource('s3')
                s3.Object(s3bucket, 'crawled_data/boxscores/' + 'boxscores_' + season + '.csv').put(Body=csv_buffer.getvalue())
        elif save_destination == "wasb":
                wasbaccountname = os.environ['wasbaccountname']
                containername = os.environ['containername']
                wasbaccountkey = os.environ['wasbaccountkey']
                csv_buffer = StringIO()
                result.to_csv(csv_buffer, index=False, sep=';')
                block_blob_service = BlockBlobService(
                        account_name=wasbaccountname,
                        account_key=wasbaccountkey)
                block_blob_service.create_blob_from_text(containername, 'boxscores/' + 'boxscores_' + season + '.csv', csv_buffer.getvalue())

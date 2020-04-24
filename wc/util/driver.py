from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from xvfbwrapper import Xvfb

def get_driver(path):
    vdisplay = Xvfb()
    vdisplay.start()

    # prepare Chrome driver
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)

    return driver
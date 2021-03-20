"""
Put in all the chrome webdriver requests into a single place


"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import warnings
warnings.filterwarnings('ignore')
import os
import time
os.environ['WDM_LOG_LEVEL'] = '0'


while True:
    try:
        chromeinstaller=ChromeDriverManager().install()
        break
    except Exception as e0:
        checkvalue=str(e0)
        if "API rate limit exceeded" in checkvalue:
            raise ValueError("You've exceeded the Github API Rate limit for running the installers for webdrivers. Please wait an hour and try again")
            break
        else:
            print("Cannot install chromedriver")
            break


def chrome(headless=False):
    try:
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument('user-agent=' + str(UserAgent().random) + '')
        options.add_argument("--incognito")
        options.add_argument("--ignore_certificate_errors")
        driver = webdriver.Chrome(chromeinstaller,chrome_options=options)
        return driver
    except Exception as e:
        print("failure in chrome function")
        print(e)
        return None

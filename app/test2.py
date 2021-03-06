import tkinter as tk
import threading
import os
import time, string, random

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from multiprocessing.pool import ThreadPool


browsers = []

class Browser:
    def __init__(self, url, session_file):
        self.url = url
        self.session_file = session_file


def manipulate_browser(browser):
    global lock
    with lock:
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "none"

        chrome_options = webdriver.ChromeOptions();

        current_dir = os.path.dirname(os.path.abspath(__file__))
        os.mkdir(current_dir + '\\' + browser.session_file) 
        chrome_options.add_argument(r'--user-data-dir=' + current_dir + '\\' + browser.session_file + '\\selenium')

        chrome_options.add_argument("--window-size=750,750")

    browser.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options, desired_capabilities=caps)

    while True:
        browser.driver.get(browser.url)
        time.sleep(4)



def start_browsers():

    for browser in browsers:
        browser.thread = threading.Thread(target=manipulate_browser, args=(browser,))
        browser.thread.start()


if __name__=='__main__':
    lock = threading.Lock()
    threads = []
    urls = 'https://google.com', 'https://facebook.com', 'https://instagram.com', 'https://snapchat.com', 'https://stackoverflow.com', 'https://amazon.com', 'https://microsoft.com'#, 'https://stackoverflow.com', 'https://youtube.com', 'https://yahoo.com'
    for url in urls:
        session_file = 'session_' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        newBrowser = Browser(url, session_file)
        browsers.append(newBrowser)


    root = tk.Tk()                    
    button_start_browsers = tk.Button(root, command=start_browsers, width=50, height=4, bg='red', text='Start Browsers')
    button_start_browsers.pack()
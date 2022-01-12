from bs4 import BeautifulSoup
import urllib.request
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import json
import re
import time
import requests
import uuid
import os
from termcolor import colored
from selenium.webdriver.common.keys import Keys

class TheImageFetcher:
    def set_chrome_driver(self, chromedriver_path):
        self.chromedriver_path = chromedriver_path

    def set_url_stem(self, query):
        query = query.replace(" ", "+")
        url_stem = "https://www.google.com/search?q="+query+"&source=lnms&tbm=isch"+self.search_mode
        self.url_stem = url_stem

    def fetch_images(self, query, loading_time=5, dir_name="images", create_source_file=False, file_type="jpg", print_progress=True, search_mode=""):
        self.create_source_file = create_source_file
        self.file_type = file_type
        self.print_progress = print_progress
        self.search_mode = search_mode
        dir_name.replace(" ", "_")
        self.set_url_stem(query)
        url = self.url_stem
        chrome_options = Options()
        # Opens the browser up in background
        chrome_options.add_argument("--headless")
        browser = Chrome(options=chrome_options,
                         executable_path=self.chromedriver_path)
        browser.get(url)
        html = browser.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        time.sleep(4)
        html = browser.page_source

        soup = BeautifulSoup(html, 'html.parser')
        counter = 0
        image_divs = soup.find_all(name='script')
        image_urls = []
        try:
            os.mkdir(dir_name)
        except:
            print(colored('WARNING: This folder named '+dir_name+' has already been created. This can lead to errors because duplicates can occur.', 'red'))
        for div in image_divs:
              txt = str(div)
              if 'AF_initDataCallback' not in txt:
                  continue
              if 'ds:0' in txt or 'ds:1' not in txt:
                  continue
              uris = re.findall(r'http.*?\.(?:jpg|jpeg)', txt)
              image_urls = uris+ image_urls
        for image in image_urls:
            counter += 1
            if self.print_progress is True:
                print("progress:", '{:.1%}'.format(counter/len(image_urls)))
            self.save_image_to_dir("https://"+image.split('["https://')[-1], dir_name, uuid.uuid4())

    def save_image_to_dir(self, url, dir_name, file_name):
        try:
             request = urllib.request.urlopen(url, timeout=5)
             with open(dir_name+"/"+str(file_name)+"."+self.file_type, 'wb') as f:
                try:
                   f.write(request.read())
                   self.save_to_source_file(url, dir_name+"/"+str(file_name)+"."+self.file_type)
                except:
                   print("error")
        except:
             pass

    def save_to_source_file(self, url, dir):
        if self.create_source_file is True:
          log_file = open('sources.txt', 'a+')
          log_file.write(dir+" extracted from "+url+"\n")

TheImageFetcher = TheImageFetcher()
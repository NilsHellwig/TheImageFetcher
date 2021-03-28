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

class TheImageFetcher:
    def set_chrome_driver(self, chromedriver_path):
        self.chromedriver_path = chromedriver_path

    def set_url_stem(self, query):
        query = query.replace(" ", "+")
        url_stem = "https://www.google.de/search?q="+query+"&source=lnms&tbm=isch"
        self.url_stem = url_stem

    def fetch_images(self, query, iterations=1, loading_time=5, dir_name="images", create_source_file=False, file_type="jpg", print_progress=True):
        self.create_source_file = create_source_file
        self.file_type = file_type
        self.print_progress = print_progress
        self.set_url_stem(query)
        dir_name.replace(" ", "_")
        url = self.url_stem
        chrome_options = Options()
        # Opens the browser up in background
        chrome_options.add_argument("--headless")
        browser = Chrome(options=chrome_options,
                         executable_path=self.chromedriver_path)
        browser.get(url)
        for i in range(iterations):
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        counter = 0
        ids = soup.find_all("div", {"data-id": re.compile(r"\b\w{14}\b")})
        saved_ids = []
        for a in ids:
            counter += 1
            element_soup = BeautifulSoup(str(a), "html.parser")
            for meta in element_soup:
                saved_ids.append(meta.attrs['data-id'])
        self.get_image_urls(saved_ids, dir_name)

    def get_image_urls(self, image_ids, dir_name):
        image_urls = []
        counter = 0
        try:
            os.mkdir(dir_name)
        except:
            print(colored('WARNING: This folder named '+dir_name+' has already been created. This can lead to errors because duplicates can occur.', 'red'))
        for image_id in image_ids:
            counter += 1
            chrome_options = Options()
            # Opens the browser up in background
            chrome_options.add_argument("--headless")
            browser = Chrome(options=chrome_options,
                             executable_path=self.chromedriver_path)
            browser.get(self.url_stem+"#imgrc="+image_id)
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            ids = soup.select('div > div > div > div > div > a > img')
            for id in ids:
                element_soup = BeautifulSoup(str(id), "html.parser")
                for meta in element_soup:
                    if meta.attrs['src'].startswith("https://encrypted") == False and meta.attrs['src'].startswith("data:image") == False:
                        if self.print_progress is True:
                            print("progress:", '{:.1%}'.format(counter/len(image_ids)))
                        image_urls.append(meta.attrs['src'])
                        self.save_image_to_dir(
                            meta.attrs['src'], dir_name, uuid.uuid4())
        return image_urls

    def save_image_to_dir(self, url, dir_name, file_name):
        try:
            urllib.request.urlretrieve(url, dir_name+"/"+str(file_name)+"."+self.file_type)
            self.save_to_source_file(url, dir_name+"/"+str(file_name)+"."+self.file_type)
        except:
            pass

    def save_to_source_file(self, url, dir):
        if self.create_source_file is True:
          log_file = open('sources.txt', 'a+')
          log_file.write(dir+" extracted from "+url+"\n")

TheImageFetcher = TheImageFetcher()
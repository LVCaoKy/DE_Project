# Import Library that necessary
import pandas as pd
import numpy as np
import re
from time import sleep

# Import Library for use MongoDB
from pymongo import MongoClient


# Import Library from selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException , ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
options = Options()
options.page_load_strategy = 'eager'
options.headless = True
options.add_argument(r"--user-data-dir=C:\\Users\\USER\AppData\\Local\\Google\\Chrome\\User Data\Default")
options.add_argument("--disable-javascript")
options.add_argument("--blink-settings=imagesEnabled=false")

class TGDD(webdriver):

    def __init__(self):
        super().init()
        self.get("https://batdongsan.com.vn/nha-dat-ban-tp-hcm")
        self.Chrome(options=options)
        self.result = []
        self.crawl_data()
        
    def getlinks(self):
        WebDriverWait(self, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 
            '.content-item .text .ct_title a'))
        )

        text = self.find_elements(By.CSS_SELECTOR,
        '.content-item .text .ct_title a')
        return [i.get_attribute('href') for i in text]
    def get_nextPage(self):
        current=int(driver.find_element(By.CSS_SELECTOR,'.page a.active').text)
        listNext_page = driver.find_elements(By.CSS_SELECTOR,'.page a')
        return [x.get_attribute('href') for x in listNext_page][current]
    def crawl_data(self):
        while 1:
            for x in self.getlinks():
                self.get(x)
                test = pd.Series()
                link = str(link) 
                test['Link'] = link
                test['Title'] = driver.find_element(By.CSS_SELECTOR,'h1.re__pr-title').text
                test['Address'] = driver.find_element(By.CSS_SELECTOR,'.js__pr-address').text

                # Thử lấy dữ liệu xác thực
                try:
                    test['Check'] = driver.find_element(By.CSS_SELECTOR,
                    '.js__product-detail-web .re__pr-stick-listing-verified .re__text').text
                    
                except NoSuchElementException :
                    test['Check']='Chưa Xác Thực'
                test['BusinessForm'] = driver.find_element(By.CSS_SELECTOR,".js__ob-breadcrumb").get_attribute('title')
                # Thử lấy dữ liệu chi tiêt về mẫu
                name_data = driver.find_elements(By.CSS_SELECTOR,

                '.js__li-specs  .js__section-body .js__other-info .re__pr-specs-content-item .re__pr-specs-content-item-title')
                value_data =  driver.find_elements(By.CSS_SELECTOR,

                '.js__li-specs  .js__section-body .js__other-info .re__pr-specs-content-item .re__pr-specs-content-item-value')
                data = pd.Series(value_data,index=name_data)

                for i in range(len(name_data)):
                    test[name_data[i].text] = value_data[i].text

                name_data_2 = driver.find_elements(By.CSS_SELECTOR,
                '.js__pr-config .js__pr-config-item .title')

                value_data_2 = driver.find_elements(By.CSS_SELECTOR,
                '.js__pr-config .js__pr-config-item .value')

                for i in range(len(name_data_2)):
                    test[name_data_2[i].text] = value_data_2[i].text

                self.result = pd.concat([self.result, test.to_frame().T], ignore_index=True)
            self.get(self.get_nextPage())
    def store(self):
        client = MongoClient("mongodb://localhost:27017/")
        db = client["batdongsan"]
        collection = self.result
        data=X.result
        data_dict = data.to_dict("records")
        collection.insert_many(data_dict)
if __name__ == "__main__":
    TGDD()
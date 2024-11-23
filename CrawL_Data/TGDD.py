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

class TGDD(webdriver):
    def __init__(self):
        super().init()
        self.get("https://www.thegioididong.com/dtdd#c=42&o=13&pi=3")
        self.result = []
        


if __name__ == "__main__":
    TGDD()
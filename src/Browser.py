from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

class Browser:
  
  def __init__(self):
    DRIVER_PATH = "/usr/bin/chromedriver"
    BRAVE_BROWSER_PATH = "/usr/bin/brave-browser"
    options = webdriver.ChromeOptions()
    options.binary_location = BRAVE_BROWSER_PATH
    options.add_argument("--incognito")
    # options.add_argument("--headless")#no graphic

    self._driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
    self._driver.implicitly_wait(10)
    self._driver.maximize_window()

  # def get_driver(self):
  #   return self.driver
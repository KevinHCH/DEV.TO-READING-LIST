from src.Browser import Browser
from pprint import pprint
import os

from dotenv import load_dotenv
load_dotenv()


class Scrapper(Browser):
  url = "https://dev.to"
  __USERNAME = os.getenv("USERNAME_GIT")
  __PASSWORD = os.getenv("PASSWORD_GIT")
  
  def __init__(self):
    super().__init__()
    self._driver.get(self.url)
  
  def login():
    pass
    
    
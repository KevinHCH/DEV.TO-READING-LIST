from src.Browser import Browser
from pathlib import Path
from pprint import pprint
import os, time, re


from dotenv import load_dotenv
load_dotenv()


class Scrapper(Browser):
  # url = "https://dev.to"
  url_login = "https://dev.to/enter"
  my_reading_list = "https://dev.to/readinglist"
  __USERNAME = os.getenv("USERNAME_GIT")
  __PASSWORD = os.getenv("PASSWORD_GIT")
  posts_links = []
  
  def __init__(self):
    super().__init__()
    self.go_to(self.url_login)
    self.login()
    time.sleep(3)
    self.posts_links = self.get_posts(5)
    
  def go_to(self, url):
    self._driver.get(url)
  
  def login(self):
    self._driver.find_element_by_css_selector(".links a:first-of-type").click()
    input_field = self._driver.find_element_by_id("login_field")
    password_field = self._driver.find_element_by_id("password")

    input_field.send_keys(self.__USERNAME)
    password_field.send_keys(self.__PASSWORD)

    self._driver.find_element_by_css_selector('input[type="submit"]').click()

    print("## Login success \n")
    self.go_to(self.my_reading_list)
  
  def get_posts(self, limit=15):
    posts = self._driver.find_elements_by_css_selector(".items-container .item-wrapper > a")
    return [post.get_attribute("href") for index, post in enumerate(posts) if index < limit]

  def save_pdf(self, path):
    import pdfkit
    for index,page in enumerate(self.posts_links):
      self.go_to(page)
      title = self._driver.find_element_by_css_selector("header h1").text.strip()
      title = re.sub(r"\s|\\|\/","_",title)
      title = re.sub(r"\.|\'|\"","",title)
      
      pdfkit.from_url(page, f"{path}/{index}_{title}.pdf")

  def merge_all_pdfs(self, full_path):
    from PyPDF2 import PdfFileMerger
    from datetime import datetime

    path_handler = Path(full_path)
    merger = PdfFileMerger()
    complete_name = f"{datetime.now().strftime('%d_%m_%Y')}_posts"

    for pdf_file in path_handler.iterdir():
      merger.append(f"{pdf_file}")
    
    merger.write(f"{full_path}/{complete_name}.pdf")
    merger.close()


    


    
    
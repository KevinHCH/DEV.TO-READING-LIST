from src.Browser import Browser
from pathlib import Path
from pprint import pprint
from datetime import datetime
import os, time, re, json, sys
from dotenv import load_dotenv
import pdfkit

load_dotenv()

class Scrapper(Browser):
  # url = "https://dev.to"
  url_login = "https://dev.to/enter"
  my_reading_list = "https://dev.to/readinglist"
  __USERNAME = os.getenv("USERNAME_GIT")
  __PASSWORD = os.getenv("PASSWORD_GIT")
  posts_links, readed_posts, titles = [], [], []
  log_file = "readed_posts.json"

  def __init__(self):
    super().__init__()
    self.go_to(self.url_login)
    self.login()
    time.sleep(3)
    self.posts_links = self.get_posts()
    

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
  
  def write_file(self, data):
    with open(self.log_file, "w") as file:
      file.write(json.dumps(data, indent=2))
  
  def get_posts(self, limit=15):
    posts = self._driver.find_elements_by_css_selector(".items-container .item-wrapper > a")
    post_links = [post.get_attribute("href") for index, post in enumerate(posts) if index < limit]

    if not Path(self.log_file).exists():
      self.write_file(post_links)
      
    return post_links
  
  def get_readed_posts(self):
    with open(self.log_file, "r") as file:
      return json.loads(file.read())
  
  def get_unread_posts(self):
    first_list = list(set(self.posts_links) - set(self.get_readed_posts()))
    second_list = list(set(self.get_readed_posts()) - set(self.posts_links)) 
    return list(set(first_list) - set(second_list))
    

  def save_pdf(self, path):
    new_posts = self.get_unread_posts() if len(self.get_unread_posts()) > 0 else self.posts_links
    # self.posts_links = self.get_unread_posts() if len(self.get_unread_posts()) > 0 else self.posts_links
    starts_at = 1
    for index,page in enumerate(new_posts, starts_at):
      self.go_to(page)
      title = self._driver.find_element_by_css_selector("header h1").text.strip()
      self.titles.append(title)
      title = re.sub(r"\s|\\|\/","_",title)
      title = re.sub(r"\.|\'|\"","",title)
      index = f"0{index}" if index < 10 else index
      pdfkit.from_url(page, f"{path}/{index}_{title}.pdf")
    
    #update readed post
    print("## Updating reading list...")
    new_read_list = list(set(self.get_unread_posts() + self.posts_links))
    self.write_file(new_read_list)
  
  def create_index(self, full_path):
    css_path = Path(f"{Path().cwd()}/styles/style.css")
    file_name = f"{full_path}/00_index.pdf"
    today = datetime.now().strftime('%d-%m-%Y')
    render_titles = [f"<li>{title}</li>" for title in self.titles]
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@700&display=swap" rel="stylesheet">
    </head>
    <body>
      <main>
        <h1>POSTS {today}</h1>
        <section>
        <h3>Índice</h3>
          <ol>
            {''.join(render_titles)}
          </ol>
        </section>
      </main>
    </body>
    </html>
    """
    pdfkit.from_string(html_template, file_name, css=css_path)


  def merge_all_pdfs(self, full_path):
    from PyPDF2 import PdfFileMerger
    # Index creation before the merge of all PDFS
    self.create_index(full_path)

    path_handler = Path(full_path)
    merger = PdfFileMerger()
    today_date = datetime.now().strftime('%d_%m_%Y')
    complete_name = f"{today_date}_posts"

    for pdf_file in sorted(path_handler.iterdir()):
      # pprint(f"{pdf_file}")
      merger.append(f"{pdf_file}")
    
    merger.write(f"{full_path}/{complete_name}.pdf")
    merger.close()

  def __exit__(self):
    print("## Closing the browser")
    self._driver.close()


    


    
    
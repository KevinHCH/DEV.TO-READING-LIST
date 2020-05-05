from src.Scrapper import Scrapper
from src.Email import Email
from pathlib import Path
import os

def main():
  current_dir = Path().cwd()
  destiny_dir = "pdf"
  full_path = f"{current_dir}/{destiny_dir}"

  if not Path(full_path).is_dir():
    os.mkdir(full_path)
  
  scrapper = Scrapper()
  scrapper.save_pdf(full_path)
  scrapper.merge_all_pdfs(full_path)
  scrapper.__exit__()

  email = Email()
  email.set_message("Those are all post for today")
  email.set_file(full_path)
  print("## Sending email...")
  email.send_mail()


if __name__ == "__main__":
  main()

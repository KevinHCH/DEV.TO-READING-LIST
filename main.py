from src.Scrapper import Scrapper
from pathlib import Path
import os

if __name__ == "__main__":
  
  current_dir = Path().cwd()
  destiny_dir = "pdf"
  full_path = f"{current_dir}/{destiny_dir}"

  if not Path(full_path).is_dir():
    os.mkdir(full_path)
  
  scrapper = Scrapper()
  scrapper.save_pdf(full_path)
  scrapper.merge_all_pdfs(full_path)

  # -comprobar el orden, debe ser el mismo, los ultimos posts seran los primeros
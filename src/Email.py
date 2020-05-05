# EMAIL LIBS
import smtplib, ssl
from email import encoders
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header

from pprint import pprint

from datetime import datetime
# ENV VARS
from dotenv import load_dotenv
import os
load_dotenv()
class Email():
  
  def __init__(self):
    self.__MAIL_SENDER = os.getenv("MAIL_SENDER")
    self.__MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    self.__MAIL_RECEIVER = os.getenv("MAIL_RECEIVER")
    self.encoding = "utf-8"
    today_date = datetime.now().strftime("%d-%m-%Y")
    self.subject = f"READ LIST: {today_date}"

    self.message = MIMEMultipart("alternative")
    self.set_header_email()

  def set_header_email(self):
    self.message["From"] = f"DEV BOT LIST<{self.__MAIL_SENDER}>"
    self.message["To"] = self.__MAIL_RECEIVER
    self.message["Subject"] = str(Header(self.subject, self.encoding))
  
  def set_subject(self, subject):
    self.subject = subject

  def set_receiver(self, receiver):
    self.__MAIL_RECEIVER = receiver
  
  def set_html_message(self, html_template):
    self.message.attach(MIMEText(html_template, "html"))

  def set_message(self, text, message_type="plain"):
    self.message.attach(MIMEText(text, message_type, self.encoding))
  
  def set_file(self, path):
    today_date = datetime.now().strftime('%d_%m_%Y')
    complete_name = f"{today_date}_posts.pdf"
    full_path = f"{path}/{complete_name}"
    try:
      with open(full_path, "rb") as file:
        handler = MIMEBase("application", "octet-stream")
        handler.set_payload(file.read())
        encoders.encode_base64(handler)
        handler.add_header("Content-disposition", f"attachment; filename={complete_name}")

        self.message.attach(handler)
    except FileNotFoundError as error:
      print(f"ERROR: {error}")
  
  def get_email_content(self):
    return self.message.as_string()

  def send_mail(self):
    PORT = 465
    MAIL_SERVER = "smtp.gmail.com"
    mail_content = self.get_email_content()

    try:
      context = ssl.create_default_context()
      with smtplib.SMTP_SSL(MAIL_SERVER, PORT, context=context) as server:
        server.login(self.__MAIL_SENDER, self.__MAIL_PASSWORD)
        server.sendmail(self.__MAIL_SENDER, self.__MAIL_RECEIVER, mail_content)
        server.quit()
        print("## Email was successfully delivered")

    except smtplib.SMTPException as error:
      print(f"ERROR while sending email:{error}")

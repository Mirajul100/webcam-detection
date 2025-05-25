import smtplib
import os
from email.message import EmailMessage
import imghdr

PASSWORD = os.getenv("pass")
SENDER = "python3436@gmail.com"
RECEIVER = "python3436@gmail.com"

def send_mail(file_path):
    email_massage = EmailMessage()
    email_massage["Subject"] = "Person detected"
    email_massage.set_content("Hay, we just show a person / object")

    with open(file_path , "rb") as file:
        image_file = file.read()
    email_massage.add_attachment(image_file  , maintype="image" , subtype=imghdr.what(None , image_file))

    gmail = smtplib.SMTP('smtp.gmail.com' , 587)
    gmail.ehlo() # Mail server
    gmail.starttls()
    gmail.login(SENDER , PASSWORD)
    gmail.sendmail(SENDER , RECEIVER , email_massage.as_string())
    gmail.quit()

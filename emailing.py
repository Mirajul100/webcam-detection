from datetime import datetime

def email_send():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print (f"email send at {dt_string}")

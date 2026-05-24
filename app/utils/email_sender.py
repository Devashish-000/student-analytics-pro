import smtplib

def send_email(to_email, message):

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login("your_email@gmail.com", "app_password")

    server.sendmail(
        "your_email@gmail.com",
        to_email,
        message
    )

    server.quit()

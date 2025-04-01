# import smtplib
# import ssl
# import random
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from fastapi import HTTPException

# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 465
# SMTP_USERNAME = "your-email@gmail.com"
# SMTP_PASSWORD = "your-app-password"

# def send_otp(email: str, otp: str, subject: str, body: str):
#     msg = MIMEMultipart()
#     msg["From"] = SMTP_USERNAME
#     msg["To"] = email
#     msg["Subject"] = subject

#     msg.attach(MIMEText(body, "plain"))

#     context = ssl.create_default_context()

#     try:
#         with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
#             server.login(SMTP_USERNAME, SMTP_PASSWORD)
#             server.sendmail(SMTP_USERNAME, email, msg.as_string())
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error sending email: {e}")

# def generate_otp():
#     return str(random.randint(100000, 999999))

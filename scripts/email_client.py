from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib

from dotenv import load_dotenv

from logger import get_logger

logger = get_logger(__name__)

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SERVER = os.getenv("EMAIL_SERVER")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "0"))

def send_email(body: str, subject: str, receiver: list[str], sender: str = EMAIL_USER, files: list[str]=None):
    logger.info(f"Sending email {subject} to {receiver}")

    # Compose email
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ",".join(receiver)
    msg["X-Priority"] = "2"
    msg["X-MSMail-Priority"] = "High"

    # iterate all files to attach them to mail
    for f in files or []:
        logger.info(f"Attaching file: {f}")
        # attach file in email
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=os.path.basename(f),
            )
        # After the file is closed
        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(f)}"'
        msg.attach(part)

    # attach previous body to email
    msg.attach(MIMEText(body, "plain"))

    logger.info(f"Connecting to {EMAIL_SERVER}:{EMAIL_PORT}")
    # Send email
    with smtplib.SMTP_SSL(EMAIL_SERVER, EMAIL_PORT) as smtp:
        # smtp.starttls()  # Secure the connection
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)
        smtp.sendmail(sender, receiver, msg.as_string())
        logger.info("Mail successfully sent!")
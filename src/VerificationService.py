import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv


class VerificationService:
    @staticmethod
    def send_email(recipient, subject, message):
        load_dotenv()

        sender_email = os.getenv("ADMIN_EMAIL")
        sender_password = os.getenv("ADMIN_PASSWORD")

        msg = MIMEText(message, "html")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, msg.as_string())
            server.quit()
            print("\t verification code was sent to your email:")
            print(f"\t{recipient}")
        except Exception as e:
            print(f"Error: {e}")
    
    @staticmethod
    def send_text_message(recipient, message):
        """ SEND TEXT MESSAGE """

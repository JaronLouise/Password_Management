import os
import pyotp
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText


class MultiFactorAuth:
    def __init__(self, user_email):
        self.__secret = pyotp.random_base32()  # Store this for the user
        self.email = user_email
        self.__otp = None  # Store OTP for email-based verification

    def generate_totp(self):
        """Generate a TOTP for Google Authenticator."""
        totp = pyotp.TOTP(self.__secret)
        return totp.now()

    def verify_totp(self, user_input):
        """Verify the TOTP input by the user."""
        totp = pyotp.TOTP(self.__secret)
        return totp.verify(user_input)

    def send_email(self, subject, message) -> bool:
        """Generate and send a one-time password (OTP) via email."""
        load_dotenv()

        sender_email = os.getenv("ADMIN_EMAIL")
        sender_password = os.getenv("ADMIN_PASSWORD")

        try:
            msg = MIMEText(message, "html")
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = self.email

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
            return True
        except Exception:
            return False

    def verify_email_otp(self, user_input):
        """Verify the OTP input by the user."""
        return str(user_input) == str(self.__otp)


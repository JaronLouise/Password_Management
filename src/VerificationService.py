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
    def get_network(phone_number: str) -> str:
        globe_prefixes = {
            "0817", "0905", "0906", "0915", "0916", "0917", "0926", "0927",
            "0935", "0936", "0937", "0945", "0953", "0954", "0955", "0956",
            "0965", "0966", "0967", "0975", "0977", "0978", "0979", "0995",
            "0996", "0997"
        }
        
        smart_prefixes = {
            "0907", "0908", "0909", "0910", "0911", "0912", "0913", "0914",
            "0918", "0919", "0920", "0921", "0928", "0929", "0930", "0938",
            "0939", "0940", "0941", "0942", "0943", "0946", "0947", "0948",
            "0949", "0950", "0951", "0961", "0963", "0968", "0969", "0970",
            "0981", "0989", "0991", "0992", "0993", "0994", "0998", "0999"
        }

        if phone_number in globe_prefixes:
            return "GLOBE"
        elif phone_number in smart_prefixes:
            return "SMART"
        else:
            return ""

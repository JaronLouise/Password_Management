import pyotp
import smtplib
import random
from email.message import EmailMessage

class MFA:
    def __init__(self, user_email):
        self.secret = pyotp.random_base32()  # Store this for the user
        self.user_email = user_email
        self.otp = None  # Store OTP for email-based verification

    def generate_totp(self):
        """Generate a TOTP for Google Authenticator."""
        totp = pyotp.TOTP(self.secret)
        return totp.now()

    def verify_totp(self, user_input):
        """Verify the TOTP input by the user."""
        totp = pyotp.TOTP(self.secret)
        return totp.verify(user_input)

    def send_email_otp(self, sender_email, sender_password):
        """Generate and send a one-time password (OTP) via email."""
        self.otp = random.randint(100000, 999999)
        msg = EmailMessage()
        msg.set_content(f"Your OTP code is: {self.otp}")
        msg["Subject"] = "Your MFA OTP Code"
        msg["From"] = sender_email
        msg["To"] = self.user_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print("OTP sent successfully!")

    def verify_email_otp(self, user_input):
        """Verify the OTP input by the user."""
        return str(user_input) == str(self.otp)

# Example usage (Testing)
if __name__ == "__main__":
    user_email = "user_email@example.com"
    mfa = MFA(user_email)

    # Option 1: TOTP
    print("Your TOTP is:", mfa.generate_totp())
    user_totp = input("Enter TOTP: ")
    if mfa.verify_totp(user_totp):
        print("✅ TOTP Authentication Successful!")
    else:
        print("❌ Invalid TOTP!")

    # Option 2: Email OTP
    sender_email = "your_email@gmail.com"
    sender_password = "your_email_password"  # Store securely
    mfa.send_email_otp(sender_email, sender_password)

    user_otp = input("Enter Email OTP: ")
    if mfa.verify_email_otp(user_otp):
        print("✅ Email OTP Authentication Successful!")
    else:
        print("❌ Invalid Email OTP!")

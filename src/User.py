from Data import UserData
from DataFileHandler import DataFileHandler
from MultiFactorAuth import MultiFactorAuth
from email_validator import validate_email, EmailNotValidError

class User:
    def __init__(self):
        self.__user_id: str = ""
        self.username: str = ""
        self.__password: str = ""
        self._email: str = ""
        self.is_mfa_enabled: bool = False
        self._filename = "secure-pass_registered-user.txt"

    @property
    def user_id(self) -> str:
        return self.__user_id

    @property
    def password(self) -> object:
        return self.__raise_value_error()
    
    @property
    def email(self) -> str:
        return self._email

    @user_id.setter
    def user_id(self, user_id: str) -> None:
        if not self.__user_id:
            self.__user_id = user_id

    @password.setter
    def password(self, password) -> None:
        if not self.__password:
            self.__password = password

    @email.setter
    def email(self, email):
        self._email = email

    def signin(self, method) -> bool:
        file = DataFileHandler()
        file.filename = self._filename
        file.initialize_file_storage()

        if method == "USERNAME PASSWORD":
            if not file.search("username", self.username):
                raise ValueError("User is not registered.")

            stored_password = file.select("username", self.username, "password")

            return stored_password == self.__password
            
        elif method == "EMAIL OTP":
            if not file.search("email", self.email):
                raise ValueError("Email is not registed.")
            
            mfa = MultiFactorAuth(self.email)
            otp = mfa.generate_totp()

            email_subject = "SecurePass: One-Time Password (OTP)"
            email_body = f"""
                <!DOCTYPE html>
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                    <h1>Prove Your Signer Identity</h1>
                    <p>Hello {self.username},</p>
                    <p>You are required to enter the following code to sign-in in SecurePass. Please enter the code:</p>
                    <h2 style="background-color: #f4f4f4; padding: 10px; display: inline-block;">{otp}</h2>
                    <p><i>The request for this access originated from SecurePass.</i></p>
                </body>
                </html>
            """
            sent = mfa.send_email(email_subject, email_body)

            if not sent: return sent

            i_otp = input("\tOTP: ")
            return i_otp == otp


    def signup(self) -> None:
        file = DataFileHandler()

        data = self._transform_data()
        file.filename = self._filename
        file.initialize_file_storage()

        if file.search("username", self.username):
            raise ValueError("Username is already used.")

        file.insert(data)

    def signout(self):
        print("Signed-out.")
        del self

    def update_profile(self) -> bool:
        file = DataFileHandler()

        data = self._transform_data()
        file.filename = self._filename
        file.initialize_file_storage()

        if file.search("user_id", self.__user_id):
            return file.update(data)
        
    def get_user_data(self, method: str):
        file = DataFileHandler()
        file.filename = self._filename
        file.initialize_file_storage()

        if method == "USERNAME PASSWORD":
            user_data = file.select_all("username", self.username)
        elif method == "EMAIL OTP":
            user_data = file.select_all("email", self.email)
        else: return

        if user_data:
            self.username       = user_data[0]["username"]
            self._email         = user_data[0]["email"]
            self.user_id        = user_data[0]["user_id"]
            self.__password     = user_data[0]["password"]
            self.is_mfa_enabled = user_data[0]["is_mfa_enabled"]

    def verify_email(self, email: str) -> bool:
        try:
            validate_email(email)

            mfa: MultiFactorAuth = MultiFactorAuth(email)
            verification_code = mfa.generate_totp()
            email_subject = "SecurePass Email Verification"

            email_body = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Email Verification</title>
                </head>
                <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                    <h1>Verify Your Email Address</h1>
                    <p>You need to verify your email address to enable multi-factor authentication (MFA). Enter the following code to verify your email:</p>
                    <h2 style="background-color: #f4f4f4; padding: 10px; display: inline-block;">{verification_code}</h2>
                    <p><i>The request for this access originated from SecurePass.</i></p>
                </body>
                </html>
            """

            sent = mfa.send_email(email_subject, email_body)
            
            if not sent: return sent
            
            i_verification_code = input("\tVerification Code: ")
            return i_verification_code == verification_code
        except EmailNotValidError:
            print("\t❌Error: Email not accepted.")

    def __raise_value_error(self) -> object:
        raise AttributeError("Cannot access this attribute directly.")

    def _transform_data(self) -> UserData:
        user: UserData = {
            "user_id": self.__user_id,
            "username": self.username,
            "password": self.__password,
            "email": self.email,
            "is_mfa_enabled": self.is_mfa_enabled
        }
        return user

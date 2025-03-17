from Data import UserData, MfaData
from PasswordVault import PasswordVault
from DataFileHandler import DataFileHandler
from VerificationService import VerificationService
from email_validator import validate_email, EmailNotValidError

class User:
    def __init__(self):
        self.__user_id: str = ""
        self.username: str = ""
        self.__password: str = ""
        self._email: str = ""
        self._phone_number: str = ""
        self.is_mfa_enabled: bool = False

    @property
    def user_id(self) -> str:
        return self.__user_id

    @property
    def password(self) -> object:
        return self.__raise_value_error()
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def phone_number(self) -> str:
        return self._phone_number

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

    def signin(self) -> list:
        file = DataFileHandler()
        file.filename = "secure-pass_registered-user.txt"
        file.initialize_file_storage()

        if not file.search("username", self.username):
            raise ValueError("User is not registered.")

        stored_password = file.select("username", self.username, "password")

        if stored_password == self.__password:
            return file.select_all(self.username)

    def signup(self) -> None:
        file = DataFileHandler()

        data = self._transform_data()
        file.filename = "secure-pass_registered-user.txt"
        file.initialize_file_storage()

        if file.search("username", self.username):
            raise ValueError("Username is already used.")

        file.insert(data)

    def signout(self):
        print("Signed-out.")
        del self

    def verify_email(self, email: str) -> bool:
        try:
            validate_email(email)

            verification_code = PasswordVault().generate_password(6)
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

            VerificationService.send_email(
                email, 
                "SecurePass Email Verification", 
                email_body
            )
            i_verification_code = input("\tVerification Code: ")
            return i_verification_code == verification_code
        except EmailNotValidError:
            print("\t❌Error: Email not accepted.")

        def verify_phone_number(self, phone_number: str) -> bool:
            """ send text message """

    def __raise_value_error(self) -> object:
        raise AttributeError("Cannot access this attribute directly.")

    def _transform_data(self) -> UserData:
        mfa_data: MfaData = {
            "email": self._email,
            "phone_number": self._phone_number
        }

        user: UserData = {
            "user_id": self.__user_id,
            "username": self.username,
            "password": self.__password,
            "is_mfa_enabled": self.is_mfa_enabled,
            "mfa_auth": mfa_data
        }
        return user

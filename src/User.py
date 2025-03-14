import sendgrid
from sendgrid.helpers.mail import Mail
from Data import UserData, MfaData
from DataFileHandler import DataFileHandler
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
        self.__user_id = user_id

    @password.setter
    def password(self, password) -> None:
        self.__password = password

    @email.setter
    def email(self, email):
        try:
            validate_email(email)
            self.send_no_reply_email(email)

            self._email = email
        except EmailNotValidError:
            raise ValueError("Email is not valid.")

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

    def send_no_reply_email(self, email):
        sg = sendgrid.SendGridAPIClient("your_sendgrid_api_key")
        email = Mail(
            from_email="noreply@yourdomain.com",
            to_emails=email,
            subject="No-Reply Email",
            plain_text_content="This is an automated email. Please do not reply."
        )

        try:
            response = sg.send(email)
            print(f"Email sent! Status code: {response.status_code}")
        except Exception as e:
            print(f"Failed to send email: {e}")

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

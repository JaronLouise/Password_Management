from UserData import UserData
from DataFileHandler import DataFileHandler
from email_validator import validate_email, EmailNotValidError


class User:
    def __init__(self):
        self.__user_id: str = ""
        self.username: str = ""
        self._email: str = ""
        self.__password: str = ""
        self.is_mfa_enabled: bool = False

    @property
    def user_id(self) -> str:
        return self.__user_id

    @property
    def email(self) -> object:
        return self.__raise_value_error()

    @property
    def password(self) -> object:
        return self.__raise_value_error()

    @user_id.setter
    def user_id(self, user_id: str) -> None:
        self.__user_id = user_id

    @email.setter
    def email(self, email) -> None:
        try:
            validate_email(email)
            self._email = email
        except EmailNotValidError as e:
            raise ValueError(e)

    @password.setter
    def password(self, password) -> None:
        self.__password = password

    def signin(self) -> list:
        file = DataFileHandler()
        file.filename = "secure-pass_registered-user.txt"
        file.initialize_file_storage()

        if not file.search("email", self._email):
            raise ValueError("Email is not registered.")

        if file.select_password(self._email) == self.__password:
            return file.select_all(self._email)

    def signup(self) -> None:
        file = DataFileHandler()

        data = self._transform_data()
        file.filename = "secure-pass_registered-user.txt"
        file.initialize_file_storage()

        if file.search("email", self._email):
            raise ValueError("Email is already registered.")

        file.insert(data)

    def signout(self):
        print("Signed-out.")
        del self

    def __raise_value_error(self) -> object:
        raise AttributeError("Cannot access this attribute directly.")

    def _transform_data(self) -> UserData:
        user: UserData = {
            "user_id": self.__user_id,
            "username": self.username,
            "email": self._email,
            "password": self.__password,
            "is_mfa_enabled": self.is_mfa_enabled
        }
        return user

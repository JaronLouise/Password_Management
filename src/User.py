from Data import UserData
from DataFileHandler import DataFileHandler


class User:
    def __init__(self):
        self.__user_id: str = ""
        self.username: str = ""
        self.__password: str = ""
        self.is_mfa_enabled: bool = False
        self.mfa_auth_data: UserData

    @property
    def user_id(self) -> str:
        return self.__user_id

    @property
    def password(self) -> object:
        return self.__raise_value_error()

    @user_id.setter
    def user_id(self, user_id: str) -> None:
        self.__user_id = user_id

    @password.setter
    def password(self, password) -> None:
        self.__password = password

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

    def __raise_value_error(self) -> object:
        raise AttributeError("Cannot access this attribute directly.")

    def _transform_data(self) -> UserData:
        user: UserData = {
            "user_id": self.__user_id,
            "username": self.username,
            "password": self.__password,
            "is_mfa_enabled": self.is_mfa_enabled,
            "mfa_auth": {}
        }
        return user

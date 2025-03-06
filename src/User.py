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
    def email(self):
        return self.__raise_value_error()

    @property
    def password(self):
        return self.__raise_value_error()

    @user_id.setter
    def user_id(self, user_id: str):
        self.__user_id = user_id

    @email.setter
    def email(self, email):
        try:
            validate_email(email)
            self._email = email
        except EmailNotValidError as e:
            raise ValueError(e)

    @password.setter
    def password(self, password):
        self.__password = password

    def signin(self):
        """ NOT IMPLEMENTED """

    def signup(self):
        """ NOT IMPLEMENTED """

    def signout(self):
        """ NOT IMPLEMENTED """

    def __raise_value_error(self):
        raise AttributeError("Cannot access this attribute directly.")

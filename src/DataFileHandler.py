from typing import List
from pathlib import Path
from Data import UserData
from json import dump, load, JSONDecodeError


##
## NOT INCLUDED IN THE CLASS DIAGRAM BECAUSE THIS IS ONLY A TEMPORARY STORAGE.
##


class DataFileHandler:
    def __init__(self):
        self.filename: str = ""

    def initialize_file_storage(self) -> None:
        try:
            self.__file_exists()
        except FileNotFoundError:
            file_path = Path(self.filename)
            file_path.touch()

    def insert(self, data: UserData) -> bool:
        self.__file_exists()

        try:
            users: list = self.select_all()
            users.append(data)

            file_path = Path(self.filename)
            with file_path.open("w", 1, "utf-8") as file:
                dump(users, file, indent=4)
            return True
        except Exception as e:
            raise OSError(f"Insertion failed: {e}")

    def update(self, data: UserData) -> bool:
        self.__file_exists()

        users = self.select_all()
        for user in users:
            if user["user_id"] == data["user_id"]:
                user["username"] = data["username"]
                user["password"] = data["password"]
                user["email"] = data["email"]
                user["is_mfa_enabled"] = data["is_mfa_enabled"]

        file_path = Path(self.filename)
        try:
            with file_path.open("w", 1, "utf-8") as file:
                dump(users, file, indent=4)
            return True
        except Exception as e:
            raise OSError(f"Update failed: {e}")

    def select_all(self, key: str = "", value: str = "") -> List[dict]:
        file_path = Path(self.filename)

        try:
            with file_path.open("r", encoding="utf-8") as file:
                data = load(file)

            if not value and not key:
                return data

            for d in data:
                if d[key] == value:
                    return [d]

        except JSONDecodeError:
            return []

    def select(self, key, value, search_key) -> str:
        users = self.select_all()

        for user in users:
            if user[key] == value:
                return user[search_key]

    def search(self, key, value) -> bool:
        users = self.select_all()
        
        for user in users:
            if user[key] == value:
                return True

    def __file_exists(self) -> bool:
        file_path = Path(self.filename)

        if file_path.is_file() and file_path.exists():
            return True
        raise FileNotFoundError("The indicated file does not exists.")

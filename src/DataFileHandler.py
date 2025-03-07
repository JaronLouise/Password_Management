from typing import List

import UserData
from pathlib import Path
from json import dump, load, dumps, JSONDecodeError


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
                user["email"] = data["email"]
                user["password"] = data["password"]
                user["is_mfa_enabled"] = data["is_mfa_enabled"]

        file_path = Path(self.filename)
        try:
            with file_path.open("w", 0, "utf-8") as file:
                for user in users:
                    file.write(dumps(user) + "\n")
            return True
        except Exception as e:
            raise OSError(f"Update failed: {e}")

    def select_all(self, email: str = "") -> List[dict]:
        file_path = Path(self.filename)

        try:
            with file_path.open("r", encoding="utf-8") as file:
                data = load(file)

            if not email:
                return data

            for d in data:
                if d["email"] == email:
                    return [d]

        except JSONDecodeError:
            return []

    def select_password(self, email) -> str:
        users = self.select_all()

        for user in users:
            if user["email"] == email:
                return user["password"]

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

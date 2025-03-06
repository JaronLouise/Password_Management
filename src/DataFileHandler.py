import UserData
from json import dump
from pathlib import Path


class DataFileHandler:
    def __init__(self):
        self.filename: str = ""

    def initialize_file_storage(self):
        if not self.__file_exists():
            file_path = Path(self.filename)
            file_path.touch()

    def insert(self, data: UserData) -> bool:
        self.__file_exists()

        try:
            file_path = Path(self.filename)
            with file_path.open("a", 0, "utf-8") as file:
                dump(data, file, indent=1)
            return True
        except Exception as e:
            raise OSError(f"Insertion failed: {e}")

    def update(self, user_id: str, data: UserData):
        self.__file_exists()

    def __file_exists(self) -> bool:
        file_path = Path(self.filename)

        if file_path.is_file() and file_path.exists():
            return True
        raise FileNotFoundError("Operation failed. The indicated file is not ")


from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import os

class EncryptionData:
    def __init__(self, key_file="encryption.key"):
        self.key_file = key_file
        self.key = self.load_or_generate_key()
        self.fernet = Fernet(self.key)

    def load_or_generate_key(self):
        """Load encryption key or generate a new one if not existing."""
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as file:
                return file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as file:
                file.write(key)
            return key

    def encrypt(self, data: str) -> str:
        """Encrypt string data and return as string."""
        encrypted_data = self.fernet.encrypt(data.encode())
        return encrypted_data.decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt string data and return the plaintext."""
        try:
            decrypted_data = self.fernet.decrypt(encrypted_data.encode())
            return decrypted_data.decode()
        except InvalidToken:
            return "[DECRYPTION FAILED]"

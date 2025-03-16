import os
import json
import random
import string
import hashlib
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

class PasswordVault:
    def __init__(self, master_password):
        self.file_path = "vault_data.json"
        self.master_password = master_password
        self.key = self._derive_key(master_password)
        self.vault_data = self.load_vault()

    def _derive_key(self, password):
        """Derive a key from the master password using PBKDF2."""
        salt = b"some_salt"  # Store this salt securely in a real app
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256-bit key
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        # Ensure the derived key is in bytes format
        return bytes(kdf.derive(password.encode()))  # Convert to bytes explicitly


    def hash_password_sha512(self, password: str) -> str:
        """Hash the password using SHA-512 with a salt."""
        salt = os.urandom(16)  # 16-byte salt
        hashed_password = hashlib.sha512(salt + password.encode()).hexdigest()
        return salt.hex() + ":" + hashed_password

    def verify_password_sha512(self, stored_hash: str, password: str) -> bool:
        """Verify the password against the stored SHA-512 hash."""
        salt, stored_password_hash = stored_hash.split(":")
        salt = bytes.fromhex(salt)
        hashed_password = hashlib.sha512(salt + password.encode()).hexdigest()
        return hashed_password == stored_password_hash

    def hash_password_pbkdf2(self, password: str) -> str:
        """Hash the password using PBKDF2 with a salt and iteration count."""
        salt = os.urandom(16)  # 16-byte salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=64,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        derived_key = kdf.derive(password.encode())
        return salt.hex() + ":" + derived_key.hex()

    def verify_password_pbkdf2(self, stored_hash: str, password: str) -> bool:
        """Verify the password against the stored PBKDF2 hash."""
        salt, stored_key = stored_hash.split(":")
        salt = bytes.fromhex(salt)
        stored_key = bytes.fromhex(stored_key)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=64,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        derived_key = kdf.derive(password.encode())
        return derived_key == stored_key

    def store_hashed_password(self, user_id, hashed_password):
        """Store the hashed master password securely in the vault."""
        # Load existing vault data
        vault_data = self.load_vault() or {}
        if user_id not in vault_data:
            vault_data[user_id] = {}

        # Store the hashed master password securely under the user_id key
        vault_data[user_id]["master_password"] = hashed_password
        self.save_vault(vault_data)


    def _encrypt(self, data):
        """Encrypt data using AES encryption."""
        iv = os.urandom(16)  # Random IV for each encryption
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data.encode()) + padder.finalize()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return b64encode(iv + encrypted).decode('utf-8')  # Store IV + encrypted data

    def _decrypt(self, encrypted_data):
        """Decrypt data using AES decryption."""
        encrypted_data = b64decode(encrypted_data)
        iv = encrypted_data[:16]
        encrypted_data = encrypted_data[16:]

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(decrypted_data) + unpadder.finalize()
        return data.decode()

    def authenticate(self) -> bool:
        """Authenticate the master password by comparing with the stored hashed password."""
        hashed_input_password = self.hash_password_pbkdf2(self.master_password)  # Use PBKDF2
        stored_password = self.vault_data.get("master_password", None)  # Fetch the stored password
        if stored_password:
            return self.verify_password_pbkdf2(stored_password, self.master_password)
        return False  # If no password is stored, authentication fails

    def load_vault(self):
        """Load vault data from file."""
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, "r") as file:
            try:
                data = json.load(file)
                if isinstance(data, dict):
                    return data
                else:
                    return {}
            except json.JSONDecodeError:
                return {}

    def save_vault(self, data):
        """Save vault data to file."""
        if isinstance(data, dict):
            with open(self.file_path, "w") as file:
                json.dump(data, file, indent=4)

    def store_account(self, user_id, website, email, password, hash_method="pbkdf2"):
        """Store a new account in the vault."""
        vault_data = self.load_vault() or {}
        if user_id not in vault_data:
            vault_data[user_id] = {}

        if website not in vault_data[user_id]:
            vault_data[user_id][website] = []

        # Check if email already exists for the website
        for account in vault_data[user_id][website]:
            if isinstance(account, dict) and account.get("email") == email:
                return "email_exists"

        # Hash or Encrypt the password before storing it
        if hash_method == "pbkdf2":
            hashed_password = self.hash_password_pbkdf2(password)
        else:
            hashed_password = self.hash_password_sha512(password)

        # Encrypt the password before saving to vault
        encrypted_password = self._encrypt(hashed_password) 

        vault_data[user_id][website].append({
            "email": email,
            "password": encrypted_password
        })
        self.save_vault(vault_data)
        return "added"

    def update_password(self, user_id, website, email, new_password, hash_method="pbkdf2"):
        """Update the password for an existing account."""
        vault_data = self.load_vault()
        if isinstance(vault_data, dict) and user_id in vault_data and website in vault_data[user_id]:
            for account in vault_data[user_id][website]:
                if isinstance(account, dict) and account.get("email") == email:
                    # Hash the new password before updating
                    if hash_method == "pbkdf2":
                        hashed_password = self.hash_password_pbkdf2(new_password)
                    else:
                        hashed_password = self.hash_password_sha512(new_password)
                    account["password"] = hashed_password
                    self.save_vault(vault_data)
                    return "updated"
        return "not_found"

    def retrieve_account(self, user_id, website, email, hash_method="pbkdf2"):
        """Retrieve account details and decrypt the password."""
        vault_data = self.load_vault()
        accounts = vault_data.get(user_id, {}).get(website, [])

        if isinstance(accounts, list):
            for account in accounts:
                if isinstance(account, dict) and account.get("email") == email:
                    # Decrypt the password before returning
                    if hash_method == "pbkdf2":
                        # Use PBKDF2 to verify and return the password
                        decrypted_password = self._decrypt(account["password"])
                        return {
                            "email": account["email"],
                            "password": decrypted_password
                        }
                    else:
                        # For SHA-512, just return the stored hash password
                        return {
                            "email": account["email"],
                            "password": account["password"] 
                        }
        return None

    def generate_password(self, length=12):
        """Generate a random password."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def delete_account(self, user_id, website, email):
        """Delete an account from the vault."""
        vault_data = self.load_vault()
        if isinstance(vault_data, dict) and user_id in vault_data and website in vault_data[user_id]:
            website_accounts = vault_data[user_id][website]
            vault_data[user_id][website] = [account for account in website_accounts if account.get("email") != email]
            self.save_vault(vault_data)

    def delete_website(self, user_id, website):
        """Delete a website and all accounts associated with it."""
        vault_data = self.load_vault()
        if isinstance(vault_data, dict) and user_id in vault_data:
            if website in vault_data[user_id] and not vault_data[user_id][website]:
                del vault_data[user_id][website]
                self.save_vault(vault_data)

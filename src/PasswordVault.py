import os
import json
import random
import string
from EncryptionData import EncryptionData

class PasswordVault:
    def __init__(self, vault_file="vault_data.json"):
        self.vault_file = vault_file
        self.encryption = EncryptionData()
        self.vault_data = self.load_vault()

    def load_vault(self):
        """Load vault data from file, decrypting passwords inside."""
        if not os.path.exists(self.vault_file):
            return {}

        with open(self.vault_file, "r") as file:
            data = json.load(file)

        decrypted_data = {}

        for user_id, websites in data.items():
            decrypted_data[user_id] = {}
            for site, accounts in websites.items():
                decrypted_accounts = []
                for account in accounts:
                    decrypted_password = self.encryption.decrypt(account["password"])
                    decrypted_accounts.append({
                        "email": account["email"],
                        "password": decrypted_password
                    })
                decrypted_data[user_id][site] = decrypted_accounts

        return decrypted_data

    def save_vault(self, vault_data):
        """Save vault data to file, encrypting all passwords before saving."""
        encrypted_data = {}

        for user_id, websites in vault_data.items():
            encrypted_data[user_id] = {}
            for site, accounts in websites.items():
                encrypted_accounts = []
                for account in accounts:
                    # If already encrypted (looks like gibberish base64), you can skip re-encryption, or force encrypt anyway.
                    # Safe option: force re-encrypt by decrypting first if possible
                    password = account["password"]

                    # If this password is already plaintext (from memory), encrypt it:
                    if not password.startswith('gAAAA'):  # Fernet encrypted strings typically start with 'gAAAA'
                        password = self.encryption.encrypt(password)

                    encrypted_accounts.append({
                        "email": account["email"],
                        "password": password
                    })
                encrypted_data[user_id][site] = encrypted_accounts

        with open(self.vault_file, "w") as file:
            json.dump(encrypted_data, file, indent=4)

    def store_account(self, user_id, website, email, password):
        vault_data = self.load_vault()

        if not isinstance(vault_data, dict):
            vault_data = {}

        if user_id not in vault_data:
            vault_data[user_id] = {}

        if website not in vault_data[user_id]:
            vault_data[user_id][website] = []

        # Check if email already exists for the website
        for account in vault_data[user_id][website]:
            if isinstance(account, dict) and account.get("email") == email:
                return "email_exists"  # Email already exists

        # ✅ Encrypt password before storing
        encrypted_password = self.encryption.encrypt(password)

        # Add new account
        vault_data[user_id][website].append({
            "email": email,
            "password": encrypted_password
        })

        self.save_vault(vault_data)
        return "added"

    def update_password(self, user_id, website, email, new_password):
        vault_data = self.load_vault()
        if user_id in vault_data and website in vault_data[user_id]:
            for account in vault_data[user_id][website]:
                if account.get("email") == email:
                    # Encrypt the updated password
                    account["password"] = self.encryption.encrypt(new_password)
                    self.save_vault(vault_data)
                    return "updated"
        return "not_found"

    def get_stored_websites(self, user_id):
        vault_data = self.load_vault()
        user_vault = vault_data.get(user_id, {})

        if isinstance(user_vault, dict):  # Ensure it's a dictionary
            return list(user_vault.keys())  # Return website names
        return []

    def retrieve_account(self, user_id, website, email):
        vault_data = self.load_vault()
        accounts = vault_data.get(user_id, {}).get(website, [])

        for account in accounts:
            if account.get("email") == email:
                # ✅ Decrypt password before returning
                decrypted_password = self.encryption.decrypt(account["password"])
                return {
                    "email": account["email"],
                    "password": decrypted_password
                }
        return None

    def generate_password(self, length=12):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def delete_account(self, user_id, website, email):
        """Delete an account by email from a website."""
        vault_data = self.load_vault()
        if isinstance(vault_data, dict) and user_id in vault_data and website in vault_data[user_id]:
            website_accounts = vault_data[user_id][website]
            
            # Remove the account with the specified email
            vault_data[user_id][website] = [account for account in website_accounts if account.get("email") != email]

            # Save after modifying the accounts list
            self.save_vault(vault_data)

    def delete_website(self, user_id, website):
        """Delete a website if it has no accounts left."""
        vault_data = self.load_vault()
        if isinstance(vault_data, dict) and user_id in vault_data:
            # If there are no accounts left for this website, delete it
            if website in vault_data[user_id] and not vault_data[user_id][website]:
                del vault_data[user_id][website]  # Remove website
                self.save_vault(vault_data)

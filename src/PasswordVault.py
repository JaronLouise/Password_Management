import os
import json
import random
import string

class PasswordVault:
    def __init__(self):
        self.file_path = "vault_data.json"

    def load_vault(self):
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, "r") as file:
            try:
                data = json.load(file)
                if not isinstance(data, dict):  # Ensure vault data is a dictionary
                    return {}
                return data
            except json.JSONDecodeError:
                return {}

    def save_vault(self, data):
        if isinstance(data, dict):  # Ensure data is a dictionary before saving
            with open(self.file_path, "w") as file:
                json.dump(data, file, indent=4)

    def store_account(self, user_id, website, email, password):
        vault_data = self.load_vault()

        if not isinstance(vault_data, dict):  # Ensure vault data is a dictionary
            vault_data = {}

        if user_id not in vault_data:
            vault_data[user_id] = {}

        if website not in vault_data[user_id]:
            vault_data[user_id][website] = []

        # Check if email already exists for the website
        for account in vault_data[user_id][website]:
            if isinstance(account, dict) and account.get("email") == email:
                return "email_exists"  # Signal that email exists for this website

        # Otherwise, add the new account
        vault_data[user_id][website].append({
            "email": email,
            "password": password
        })

        self.save_vault(vault_data)
        return "added"

    def update_password(self, user_id, website, email, new_password):
        vault_data = self.load_vault()
        if isinstance(vault_data, dict) and user_id in vault_data and website in vault_data[user_id]:
            for account in vault_data[user_id][website]:
                if isinstance(account, dict) and account.get("email") == email:
                    account["password"] = new_password
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

        if isinstance(accounts, list):  # Ensure it's a list before iterating
            for account in accounts:
                if isinstance(account, dict) and account.get("email") == email:
                    return {
                        "email": account["email"],
                        "password": account["password"]
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

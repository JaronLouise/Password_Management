import os
import re
from uuid import uuid4
from User import User
from pwinput import pwinput
from PasswordVault import PasswordVault

def is_valid_email(email: str) -> bool:
    """Validate email format."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def is_valid_password(password: str) -> bool:
    """Check if password meets at least one of the required conditions."""
    return (re.search(r"[A-Z]", password) or 
            re.search(r"\d", password) or 
            re.search(r"[@#$%^&*()_+!~`\-=\[\]{};':\",.<>?/]", password))

def is_valid_website(website: str) -> bool:
    """Validate website format with optional 'http://', 'https://', or 'www.'"""
    website_regex = r'^(https?://|www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(/[\w-]*)*$'
    return re.match(website_regex, website) is not None

def print_validation_error(field_name: str):
    """Prints a general validation error message."""
    if field_name in ["Username", "Password"]:
        print(f"\n\t❌ {field_name} must contain at least one of the following:")
        print("\t  • Uppercase letter (A-Z)")
        print("\t  • Number (0-9)")
        print("\t  • Special character (@#$%^&* etc.)")
    else:
        print(f"\n\t❌ Invalid {field_name} format. Please enter a valid {field_name}.")

def validate_field_input(field_name: str, value: str) -> bool:
    """General validation function for email, password, username, and website."""
    if field_name == "Email":
        if not is_valid_email(value):
            print_validation_error(field_name)
            return False
    elif field_name == "Website":
        if not is_valid_website(value):
            print_validation_error(field_name)
            return False
    elif field_name in ["Username", "Password"]:
        if not (re.search(r"[A-Z]", value) or 
                re.search(r"\d", value) or 
                re.search(r"[@#$%^&*()_+!~`\-=\[\]{};':\",.<>?/]", value)):
            print_validation_error(field_name)
            return False
    return True

def landing_interface() -> int:
    """Landing page. Get user choice."""
    error_message = ""

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        layout_sections("HEADER", "SecurePass")

        print("\t[1] Signup")
        print("\t[2] Signin")
        print("\t[0] Exit")

        layout_sections("BODY")

        if error_message:
            print(f"{error_message}\n")

        choice = input("Choice: ").strip()

        if choice in ["0", "1", "2"]:
            return int(choice)

        error_message = "Invalid input. Please try again."

def signup() -> None:
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        layout_sections("HEADER", "Sign-Up")

        # Username input & validation
        user = User()
        user.username = input("\tUsername: ")

        if not validate_field_input("Username", user.username):
            input("\nPress any key to try again...")
            continue  # Restart input prompt

        # Password input & immediate validation
        while True:
            password = pwinput("\tPassword: ", mask="*")
            if validate_field_input("Password", password):
                break  # Valid password, exit loop

        # Confirm password
        confirm_password = pwinput("\tConfirm Password: ", mask="*")
        if password != confirm_password:
            print("\n\t❌ Passwords do not match. Please try again.")
            input("\nPress any key to try again...")
            continue  # Restart input prompt

        # Request and set the master password
        while True:
            master_password = pwinput("\tCreate your master password: ", mask="*")
            confirm_master_password = pwinput("\tConfirm master password: ", mask="*")
            if master_password == confirm_master_password:
                # Use PasswordVault to hash the master password and store it
                vault = PasswordVault(master_password)
                hashed_master_password = vault.hash_password_pbkdf2(master_password)  # Hash the master password using PBKDF2
                vault.store_hashed_password(user.user_id, hashed_master_password)  # Store the hashed password securely
                print("\tMaster password set successfully!")
                break
            else:
                print("\n\t❌ Passwords do not match. Please try again.")

        # Successful signup
        try:
            user.password = password  # Store plain password if needed
            user.user_id = str(uuid4())
            user.signup()  # This will handle user registration in your User class (saving username, user_id, etc.)
            print("\n✅ Registered successfully!")
            break  # Exit loop upon success
        except Exception as e:
            print(f"\n❌ Error: {e}")
        finally:
            layout_sections("FOOTER")

def signin() -> int:
    layout_sections("HEADER", "Sign-In")

    print("\t[1] Using username and password.")
    print("\t[2] Using OTP sent via email.")
    print("\t[3] Using OTP sent via phone number.")
    print("\t[0] Exit")

    layout_sections("BODY")

    return int(input("Choice: "))

def username_password_signin() -> User | None:
    layout_sections("HEADER", "Sign-In")

    try:
        user = User()
        user.username = input("Username: ")
        user.password = pwinput("Password: ", mask="*")

        data: list = user.signin()

        if data:
            user.user_id = data[0]["user_id"]
            user.username = data[0]["username"]
            user.is_mfa_enabled = data[0]["is_mfa_enabled"]

            print("Signed in successfully!")
            return user
        else:
            print("Incorrect username or password.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        layout_sections("FOOTER")

def home(user_id: str, username: str, mfa_enabled: bool):
    layout_sections("HEADER", "SecurePass - Home")

    print(f"\n\tUsername: {username}")
    print(f"\tID: {user_id}\n")

    print("\t[1] View stored accounts.")
    print("\t[2] Add new account.")
    print("\t[3] Sync to USB.")
    print("\t[4] Sync from USB.")

    if mfa_enabled:
        print("\t[5] Change multi-factor authentication.")
    else:
        print("\t[5] Enable multi-factor authentication.")

    print("\t[0] Sign-out.")
    layout_sections("BODY")

    return int(input("Choice: "))

def access_mfa_auth_data(user: User):
    layout_sections("HEADER", "SecurePass - MFA")
    
    if user.is_mfa_enabled:
        print("\t[1] Modify email.")
        print("\t[2] Modify phone number.")
    else:
        print("\t[1] Add email.")
        print("\t[2] Add phone number.")

    print("\t[0] Exit")
    layout_sections("BODY")

    return int(input("Choice: "))
  
def add_account(user_id: str):
    master_password = pwinput("\tEnter your master password: ", mask="*")
    vault = PasswordVault(master_password)  # Initialize with the master password
    layout_sections("HEADER", "Add New Account")

    try:
        # Validate website input
        website = input("\tWebsite: ").strip()
        while not validate_field_input("Website", website):  # Using the validate function
            website = input("\tWebsite: ").strip()  # Re-prompt until valid

        # Validate email input
        email = input("\tEmail: ").strip()
        while not validate_field_input("Email", email):  # Using the validate function
            email = input("\tEmail: ").strip()  # Re-prompt until valid

        # Check if the account already exists
        existing_account = vault.retrieve_account(user_id, website, email)
        if existing_account:
            choice = input("\tThis email already exists. Update password? (y/n): ").strip().lower()
            if choice == "y":
                new_password = pwinput("\tNew password: ", mask="*")
                # Validate new password
                while not validate_field_input("Password", new_password):  # Using the validate function
                    new_password = pwinput("\tNew password: ", mask="*")  # Re-prompt until valid
                vault.update_password(user_id, website, email, new_password)
                print("\nPassword updated successfully!")
            else:
                print("\nAccount addition canceled.")
        else:
            # New account: Generate or input password
            print("\n\t[1] Generate new password")
            print("\t[2] Manually enter password")
            choice = input("\tChoice: ").strip()

            if choice == "1":
                password = vault.generate_password()
                print(f"\tGenerated Password: {password}")
            elif choice == "2":
                while True:
                    password = pwinput("\tPassword: ", mask="*")
                    if validate_field_input("Password", password):  # Using the validate function
                        break
                    
            else:
                print("\n\t❌ Invalid choice. Please try again.")
                return 

            # Store the new account
            vault.store_account(user_id, website, email, password)
            print("\nAccount added successfully!")
    except Exception as e:
        print(e)
    finally:
        layout_sections("FOOTER")

def view_accounts(user_id: str):
    master_password = pwinput("\tEnter your master password: ", mask="*")
    vault = PasswordVault(master_password)

    if not vault.authenticate():
        print("Incorrect master password. Access denied.")
        return

    layout_sections("HEADER", "View Stored Accounts")
    try:
        # Using load_vault directly if there is no get_stored_websites method
        vault_data = vault.load_vault()
        websites = list(vault_data.get(user_id, {}).keys())  # Get list of websites for user_id

        if not websites:
            print("\nNo stored accounts found.")
            return
        
        print("\nStored Websites:")
        websites_to_display = []

        for website in websites:
            accounts = vault_data.get(user_id, {}).get(website, [])
            if accounts:
                websites_to_display.append(website)
            else:
                vault.delete_website(user_id, website)  # Remove website from vault if no accounts

        if not websites_to_display:
            print("\nNo websites with stored accounts.")
            return

        for i, website in enumerate(websites_to_display, 1):
            print(f"\t[{i}] {website}")

        website_choice = input("\nEnter the website to view credentials: ").strip()

        if website_choice not in websites_to_display:
            print("\nInvalid website selection.")
            return

        accounts = vault_data.get(user_id, {}).get(website_choice, [])

        if accounts:
            for account in accounts:
                print(f"\nEmail: {account['email']}")
                print(f"Password: {account['password']}")

            choice = input("\n[1] Edit account\n[2] Delete account\n[0] Go back: ").strip()

            if choice in ("1", "2"):
                master_password = input("Enter master password to confirm: ").strip()
                vault = PasswordVault(master_password)

                if not vault.authenticate():
                    print("Incorrect master password. Action denied.")
                    return

                if choice == "1":
                    edit_account(user_id, website_choice)
                elif choice == "2":
                    delete_account(user_id, website_choice, accounts)
            elif choice == "0":
                print("\nGoing back.")
        else:
            print("\nNo credentials found for this website.")
    except Exception as e:
        print(f"Error while viewing accounts: {e}")
    finally:
        layout_sections("FOOTER")
        
def edit_account(user_id: str, website: str):
    vault = PasswordVault()
    email = input("\nEnter the email of the account you want to edit: ").strip()
    
    account = vault.retrieve_account(user_id, website, email)

    if account:
        print(f"\nEditing account for {email}")
        choice = input("\n[1] Generate new password\n[2] Manually enter password: ").strip()

        if choice == "1":
            new_password = vault.generate_password()
            print(f"Generated Password: {new_password}")
        elif choice == "2":
            while True:
                new_password = input("\nEnter new password: ").strip()
                if validate_field_input("Password", new_password): 
                    break

        # Update the password
        vault.update_password(user_id, website, email, new_password)
        print("\nPassword updated successfully!")
    else:
        print("\nNo account found with this email.")

def delete_account(user_id: str, website: str, accounts: list):
    vault = PasswordVault()
    email = input("\nEnter the email of the account you want to delete: ").strip()

    # Find and remove the account
    account_to_delete = None
    for account in accounts:
        if account['email'] == email:
            account_to_delete = account
            break

    if account_to_delete:
        # Delete the account from the accounts list
        accounts.remove(account_to_delete)

        # Update the vault with the new accounts list
        vault.delete_account(user_id, website, email)

        # After deleting, check if the website has no more accounts left
        if not vault.load_vault().get(user_id, {}).get(website):
            # Delete the website if there are no accounts left
            vault.delete_website(user_id, website)
            print(f"\nNo accounts left for {website}. It has been removed from the vault.")
        else:
            print("\nAccount deleted successfully!")
    else:
        print("\nAccount not found.")

def layout_sections(section: str, section_name: str = "") -> None:
    length = 60
    if section == "HEADER" and section_name:
        print("\033c", end="")
        print('=' * length)
        print(section_name.center(length))
        print('=' * length + "\n")
    elif section == "FOOTER":
        print("\n" + "=" * length)
        input("Press any key to continue.")
        print("\033c", end="")
    elif section == "BODY":
        print(f"\n{'=' * length}")

from uuid import uuid4
from User import User
from pwinput import pwinput


def landing_interface() -> int:
    layout_sections("HEADER", "SecurePass")

    print("\t[1] Signup")
    print("\t[2] Signin")
    print("\t[0] Exit")

    layout_sections("BODY")

    return int(input("Choice: "))


def signup() -> None:
    layout_sections("HEADER", "Sign-In")

    try:
        user = User()
        user.username = input("\tUsername: ")
        password = pwinput("\tPassword: ", mask="*")
        confirm_password = pwinput("\tConfirm Password: ", mask="*")

        if password != confirm_password:
            raise Exception("Passwords aren't matching.")

        user.password = password
        user.user_id  = str(uuid4())

        user.signup()
        print("Registered successful!")
    except Exception as e:
        print(e)
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


def username_password_signin() -> User:
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

            print("Signed-in successful!")
            return user
        else:
            print("Incorrect password.")
    except Exception as e:
        print(e)
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
        print("\t[5] Changed multi-factor authentication.")
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


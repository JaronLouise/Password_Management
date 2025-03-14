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
        user.username = input("Username: ")
        password = pwinput("Password: ", mask="*")
        confirm_password = pwinput("Confirm Password: ", mask="*")

        if password != confirm_password:
            raise Exception("Passwords aren't matching.")

        user.user_id  = str(uuid4())

        user.signup()
        print("Registered successful!")
        layout_sections("FOOTER")

    except Exception as e:
        print(e)


def signin() -> int:
    layout_sections("HEADER", "Sign-In")

    print("\t[1] Using username and password.")
    print("\t[2] Using OTP sent via email.")
    print("\t[3] Using OTP sent via contact number.")
    print("\t[0] Exit")

    layout_sections("BODY")

    return int(input("Choice: "))


def username_password_signin() -> User:
    layout_sections("HEADER", "Sign-In")

    try:
        user = User()
        user.username = input("Username: ")
        user.password = input("Password: ")

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
        layout_sections("FOOTER")


def home():
    layout_sections("HEADER", "SecurePass - Home")

    print("\t[1] View stored accounts.")
    print("\t[2] Add new account.")
    print("\t[3] Sync to USB.")
    print("\t[4] Sync from USB.")
    print("\t[0] Sign-out.")

    return int(input("Choice: "))


def layout_sections(section: str, section_name: str = "") -> None:
    length = 52

    if section == "HEADER" and section_name:
        print("\n" * length)
        print('=' * length)
        print(section_name.center(length))
        print('=' * length + "\n")
    elif section == "FOOTER":
        print("\n" + "=" * length)
        input("Press any key to continue.")
        print("\n" * length)
    elif section == "BODY":
        print(f"\n{'=' * length}")


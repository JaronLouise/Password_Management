from uuid import uuid4
from User import User


def landing_interface() -> int:
    print(f"{'=' * 52}\n{' ' * 20} SecurePass {' ' * 20}\n{'=' * 52}\n")

    print("\t[1] Signup")
    print("\t[2] Signin")
    print("\t[0] Exit")

    print(f"\n{'=' * 52}")

    return int(input("Choice: "))


def signup() -> None:
    print("\nSIGN-UP")

    try:
        user = User()
        user.username = input("Username: ")
        user.email    = input("Email: ")
        user.password = input("Password: ")
        user.user_id  = str(uuid4())

        user.signup()
        print("Registered successful!")

    except Exception as e:
        print(e)


def signin() -> User:
    print("\nSIGN-IN")

    try:
        user = User()
        user.email = input("Email: ")
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


def home():
    print("\n" * 100)
    print(f"{'=' * 52}\n{' ' * 20} SecurePass - Home {' ' * 20}\n{'=' * 52}\n")

    print("\t[1] View stored accounts.")
    print("\t[2] Add new account.")
    print("\t[3] Sync to USB.")
    print("\t[4] Sync from USB.")
    print("\t[0] Sign-out.")

    print(f"\n{'='*52}")

    return int(input("Choice: "))

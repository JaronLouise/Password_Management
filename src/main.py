import UserInterface
from User import User


def main() -> None:
    while True:
        try:
            choice: int = UserInterface.landing_interface()

            if not 0 <= choice <= 2:
                print("Choice must in range 0-2.")

            match choice:
                case 1:
                    UserInterface.signup()
                case 2:
                    choice: int = UserInterface.signin()

                    match choice:
                        case 1:
                            user: User = UserInterface.username_password_signin()

                            if not user: continue

                            while True:
                                choice: int = UserInterface.home(user.user_id, user.username, user.is_mfa_enabled)

                                match choice:
                                    case 1:
                                        print("View stored accounts.")
                                    case 2:
                                        print("Add new account.")
                                    case 3:
                                        print("Sync to USB.")
                                    case 4:
                                        print("Sync from USB.")
                                    case 5: 
                                        choice: int = UserInterface.access_mfa_auth_data(user)

                                        match choice:
                                            case 1:
                                                UserInterface.layout_sections("HEADER", "SecurePass - Add Email")
                                                email = input("\tEmail: ")

                                                user.email = email

                                                UserInterface.layout_sections("FOOTER")
                                    case 0:
                                        user.signout()
                                        break
                        case 2:
                            print("sign in with email.")
                        case 3:
                            print("sign in using contact number.")
                case 0:
                    exit(1)

        except ValueError:
            print("Enter a number in range 0-2.")


if __name__ == "__main__":
    main()

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
                    user: User = UserInterface.signin()
                    choice: int = UserInterface.home()

                    match choice:
                        case 1:
                            print("View stored accounts.")
                        case 2:
                            print("Add new account.")
                        case 3:
                            print("Sync to USB.")
                        case 4:
                            print("Sync from USB.")
                        case 0:
                            user.signout()
                case 0:
                    exit(1)

            print("Press any key to continue...\n", end="")
            input()

        except ValueError:
            print("Enter a number in range 0-2.")


if __name__ == "__main__":
    main()

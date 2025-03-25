#main.py
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
                        case 2:
                            user: User = UserInterface.email_otp_signin()
                        case 0: 
                            continue

                    if not user: continue
                    UserInterface.home_redirects(user)
                    
                case 0:
                    exit(1)

        except ValueError:
            print("Enter a number in range 0-2.")


if __name__ == "__main__":
    main()

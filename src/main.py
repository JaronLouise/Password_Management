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
                                        UserInterface.view_accounts(user.user_id)
                                    case 2:
                                        UserInterface.add_account(user.user_id)
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

                                                verified = user.verify_email(email)
                                                if verified:
                                                    print("\t✅ Email successfully added.")
                                                else:
                                                    while True:
                                                        print("\t❌ Error verifying email.")
                                                        print("\t[1] Resend Verification.")
                                                        print("\t [0] Exit")
                                                        UserInterface.layout_sections("BODY")
                                                        choice = int(input("Choice: "))

                                                        if choice == 0: break
                                                    
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

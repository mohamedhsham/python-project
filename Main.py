from auth import users, register, login
from operations import (
    show_balance,
    link_card,
    remove_card,
    deposit,
    withdraw,
    transfer,
    show_transactions,
    show_last_5_transactions
)


def user_menu(username):
    user = users[username]

    while True:
        print("\n--- Main Menu ---")
        print("1. View Balance")
        print("2. Link Card")
        print("3. Remove Card")
        print("4. Deposit")
        print("5. Withdraw")
        print("6. Transfer")
        print("7. Transaction History")
        print("8. Last 5 Transactions")
        print("9. Logout")

        choice = input("Choose: ")

        if choice == "1":
            show_balance(user)

        elif choice == "2":
            link_card(user)

        elif choice == "3":
            remove_card(user)

        elif choice == "4":
            deposit(user)

        elif choice == "5":
            withdraw(user)

        elif choice == "6":
            transfer(user, username, users)

        elif choice == "7":
            show_transactions(user)

        elif choice == "8":
            show_last_5_transactions(user)

        elif choice == "9":
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice.")


while True:
    print("\n--- InstaPay ---")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Choose: ")

    if choice == "1":
        register()

    elif choice == "2":
        username = login()

        if username is not None:
            user_menu(username)

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")

from datetime import date
from validation import validate_amount, validate_card_number, validate_cvv


TRANSFER_FEE = 5
DAILY_TRANSFER_LIMIT = 10000


def show_balance(user):
    print("\n--- Balance ---")
    print("Current Balance:", user["balance"], "EGP")


def link_card(user):
    print("\n--- Link Visa Card ---")

    card_number = input("Enter card number: ")

    while not validate_card_number(card_number):
        print("Invalid card number.")
        card_number = input("Enter card number again: ")

    for card in user["cards"]:
        if card["card_number"] == card_number:
            print("This card is already linked.")
            return

    holder_name = input("Enter card holder name: ")
    expiry_date = input("Enter expiry date: ")

    cvv = input("Enter CVV: ")

    while not validate_cvv(cvv):
        print("Invalid CVV.")
        cvv = input("Enter CVV again: ")

    new_card = {
        "card_number": card_number,
        "holder_name": holder_name,
        "expiry_date": expiry_date,
        "cvv": cvv
    }

    user["cards"].append(new_card)

    print("Card linked successfully!")
    print("Total linked cards:", len(user["cards"]))


def remove_card(user):
    print("\n--- Remove Card ---")

    if len(user["cards"]) == 0:
        print("No linked cards.")
        return

    for index in range(len(user["cards"])):
        card = user["cards"][index]
        print(index + 1, "-", "Card ending in", card["card_number"][-4:])

    try:
        choice = int(input("Choose card to remove: "))
    except ValueError:
        print("Invalid choice.")
        return

    if choice < 1 or choice > len(user["cards"]):
        print("Invalid choice.")
        return

    confirmation = input("Are you sure you want to remove this card? yes/no: ")

    if confirmation.lower() != "yes":
        print("Card removal cancelled.")
        return

    removed_card = user["cards"].pop(choice - 1)

    print("Card ending in", removed_card["card_number"][-4:], "removed successfully.")


def deposit(user):
    print("\n--- Deposit ---")

    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount.")
        return

    if not validate_amount(amount):
        print("Amount must be greater than 0.")
        return

    user["balance"] += amount

    transaction = {
        "type": "Deposit",
        "amount": amount
    }

    user["transactions"].append(transaction)

    print("Deposit successful!")
    print("New Balance:", user["balance"], "EGP")


def withdraw(user):
    print("\n--- Withdraw ---")

    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount.")
        return

    if not validate_amount(amount):
        print("Amount must be greater than 0.")
        return

    if amount > user["balance"]:
        print("Insufficient balance.")
        return

    user["balance"] -= amount

    transaction = {
        "type": "Withdraw",
        "amount": amount
    }

    user["transactions"].append(transaction)

    print("Withdrawal successful!")
    print("Remaining Balance:", user["balance"], "EGP")


def transfer(user, username, users):
    print("\n--- Transfer ---")

    recipient_username = input("Recipient username: ")

    if recipient_username not in users:
        print("Recipient does not exist.")
        return

    if recipient_username == username:
        print("You cannot transfer money to yourself.")
        return

    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount.")
        return

    if not validate_amount(amount):
        print("Amount must be greater than 0.")
        return

    today = str(date.today())

    if user["last_transfer_date"] != today:
        user["daily_transfer_amount"] = 0
        user["last_transfer_date"] = today

    if user["daily_transfer_amount"] + amount > DAILY_TRANSFER_LIMIT:
        remaining_limit = DAILY_TRANSFER_LIMIT - user["daily_transfer_amount"]
        print("Daily transfer limit exceeded.")
        print("Remaining daily limit:", remaining_limit, "EGP")
        return

    total_amount = amount + TRANSFER_FEE

    if total_amount > user["balance"]:
        print("Insufficient balance.")
        print("Transfer amount:", amount, "EGP")
        print("Transfer fee:", TRANSFER_FEE, "EGP")
        print("Total required:", total_amount, "EGP")
        return

    print("Transfer fee:", TRANSFER_FEE, "EGP")
    print("Total deducted:", total_amount, "EGP")

    confirmation = input("Confirm transfer? yes/no: ")

    if confirmation.lower() != "yes":
        print("Transfer cancelled.")
        return

    recipient = users[recipient_username]

    user["balance"] -= total_amount
    recipient["balance"] += amount
    user["daily_transfer_amount"] += amount

    sender_transaction = {
        "type": "Transfer",
        "amount": amount,
        "fee": TRANSFER_FEE,
        "to": recipient_username
    }

    receiver_transaction = {
        "type": "Received",
        "amount": amount,
        "from": username
    }

    user["transactions"].append(sender_transaction)
    recipient["transactions"].append(receiver_transaction)

    print("Transfer successful!")
    print("Your new balance:", user["balance"], "EGP")
    print("Transferred today:", user["daily_transfer_amount"], "/", DAILY_TRANSFER_LIMIT, "EGP")


def print_transaction(transaction):
    if transaction["type"] == "Deposit":
        print("Deposit +", transaction["amount"], "EGP")

    elif transaction["type"] == "Withdraw":
        print("Withdraw -", transaction["amount"], "EGP")

    elif transaction["type"] == "Transfer":
        print(
            "Transfer -",
            transaction["amount"],
            "EGP to",
            transaction["to"],
            "| Fee:",
            transaction.get("fee", 0),
            "EGP"
        )

    elif transaction["type"] == "Received":
        print(
            "Received +",
            transaction["amount"],
            "EGP from",
            transaction["from"]
        )


def show_transactions(user):
    print("\n--- Transaction History ---")

    if len(user["transactions"]) == 0:
        print("No transactions found.")
        return

    for transaction in user["transactions"]:
        print_transaction(transaction)


def show_last_5_transactions(user):
    print("\n--- Last 5 Transactions ---")

    if len(user["transactions"]) == 0:
        print("No transactions found.")
        return

    last_five = user["transactions"][-5:]

    for transaction in last_five:
        print_transaction(transaction)

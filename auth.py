from validation import validate_username, validate_password, validate_phone


users = {}       # application database.


def find_user(username):

    if username in users:
        return users[username]

    return None


def register():      # enter new key value.

    print("\n--- Register ---")

    name = input("Enter full name: ")
    phone = input("Enter phone number: ")

    while not validate_phone(phone):    
        print("Invalid phone number.")
        phone = input("Enter phone number again: ")

    username = input("Enter username: ")

    while not validate_username(username, users):
        print("Invalid username or username already exists.")
        username = input("Enter username again: ")

    password = input("Enter password: ")

    while not validate_password(password):
        print("Password must be at least 6 characters.")
        password = input("Enter password again: ")

    users[username] = {
        "name": name,
        "phone": phone,
        "password": password,
        "balance": 0,
        "cards": [],
        "transactions": [],
        "daily_transfer_amount": 0,
        "last_transfer_date": None
    }

    print("\nRegistration successful!")


def login():
    print("\n--- Login ---")

    attempts = 3

    while attempts > 0:
        username = input("Username: ")
        password = input("Password: ")

        user = find_user(username)

        if user is not None and user["password"] == password:
            print("\nLogin successful!")
            print("Welcome", user["name"])
            return username

        attempts -= 1
        print("Invalid username or password.")

        if attempts > 0:
            print("Attempts remaining:", attempts)

    print("\nToo many failed login attempts.")
    return None

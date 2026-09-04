def validate_username(username, users):
    if username == "":
        return False

    if username in users:
        return False

    return True


def validate_password(password):
    if len(password) >= 6:
        return True

    return False


def validate_phone(phone):
    if len(phone) != 11:
        return False

    if not phone.isdigit():
        return False

    if not phone.startswith("01"):
        return False

    return True


def validate_amount(amount):
    if amount > 0:
        return True

    return False


def validate_card_number(card_number):
    if len(card_number) != 16:
        return False

    if not card_number.isdigit():
        return False

    return True


def validate_cvv(cvv):
    if len(cvv) != 3:
        return False

    if not cvv.isdigit():
        return False

    return True
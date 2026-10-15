
def get_current_date_time():
    """
    Returns the current date and time in a human-readable format.
    """
    from datetime import datetime
    return datetime.now().strftime("%m-%d-%Y %H:%M:%S")

def get_roll_dice():
    """
    Simulates rolling a six-sided dice and returns the result.
    """
    import random
    return random.randint(1, 6)

def get_generate_password(length=12):
    """
    Generates a random password of specified length.
    The password includes uppercase, lowercase, digits, and special characters.
    """
    import random
    import string

    if length < 4:
        raise ValueError("Password length should be at least 4 characters.")

    # Ensure the password has at least one character from each category
    password_chars = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]

    # Fill the rest of the password length with random choices from all categories
    all_chars = string.ascii_letters + string.digits + string.punctuation
    password_chars += random.choices(all_chars, k=length - 4)

    # Shuffle the resulting list to ensure randomness and convert to string
    random.shuffle(password_chars)
    return ''.join(password_chars)
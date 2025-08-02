import re

def is_valid_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def is_valid_phone(phone):
    return bool(re.match(r"^\+?\d{10,15}$", phone))

def is_valid_username(username):
    return bool(re.match(r"^[\w\d]{3,}$", username))

def is_valid_birthdate(date):
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date))

def is_valid_name(name):
    return len(name.strip()) >= 2

def is_valid_password(password):
    errors = []
    if len(password) < 8:
        errors.append("Minimum 8 karakter")
    if not any(c.islower() for c in password):
        errors.append("Legalább egy kisbetű")
    if not any(c.isupper() for c in password):
        errors.append("Legalább egy nagybetű")
    if not any(c.isdigit() for c in password):
        errors.append("Legalább egy számjegy")
    return errors
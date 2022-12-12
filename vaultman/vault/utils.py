import string
from secrets import choice

def password_generator(length=8):
    """custom password generator with random letters and numbers, takes a len argument"""
    letters = string.ascii_letters
    numbers = string.digits
    punctuation = string.punctuation
    alphabet = letters + numbers + punctuation

    passw = ""
    while len(passw) < length:
        passw += "".join(choice(alphabet))

    return passw


def format_uri(uri):
    if not uri:
        return ""
    prefix = "https://"
    if prefix not in uri:
        uri = prefix + uri

    return uri
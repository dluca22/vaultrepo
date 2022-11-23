import string
from secrets import choice

def password_generator(size=8):
    """this is a custom funciton in another file so that i can later add another app just designed to build passwords or passphrases"""
    letters = string.ascii_letters
    numbers = string.digits
    punctuation = string.punctuation
    alphabet = letters + numbers + punctuation

    passw = ""
    while len(passw) < size:
        passw += "".join(choice(alphabet))

    return passw

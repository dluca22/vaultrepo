import string
from secrets import choice

def password_generator(size=8):



    letters = string.ascii_letters
    numbers = string.digits
    punctuation = string.punctuation
    alphabet = letters + numbers + punctuation

    passw = ""
    while len(passw) < size:
        passw += "".join(choice(alphabet))

    return passw

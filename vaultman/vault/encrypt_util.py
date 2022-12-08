
from cryptography.fernet import Fernet
import base64
import logging
import traceback
from django.conf import settings


def encrypt(field):
    try:
        field = str(field)
        cipher_field = Fernet(settings.ENCRYPT_KEY)
        encrypt_field = cipher_field.encrypt(field.encode('ascii'))
        encrypt_field = base64.urlsafe_b64encode(encrypt_field).decode("ascii")
        return encrypt_field
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def decrypt(field):
    try:
        field = base64.urlsafe_b64decode(field)
        cypher_key = Fernet(settings.ENCRYPT_KEY)
        decode_field = cypher_key.decrypt(field).decode("ascii")
        return decode_field
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None
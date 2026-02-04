import base64
import hashlib
import os


def generate_session_keys():
    api_key = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode()
    hashed_api_key = hash_key(api_key.encode())

    return api_key, hashed_api_key


def hash_key(key: bytes):
    hashed_key = hashlib.sha256(key).digest()
    return base64.b64encode(hashed_key).decode()

import base64
import hashlib
import os


def generate_session_id():
    api_key = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode()
    return api_key


def hash_key(key: bytes):
    hashed_key = hashlib.sha256(key).digest()
    return base64.b64encode(hashed_key).decode()

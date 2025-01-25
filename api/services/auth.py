import hashlib
import hmac
from urllib.parse import parse_qsl

from data.config import TELEGRAM_BOT_TOKEN


def is_telegram(query_string: str) -> bool:
    data = {}
    parsed_data = parse_qsl(query_string)
    for k, v in parsed_data:
        data[k] = v

    sorted_data = dict(sorted(data.items()))
    hash = sorted_data.pop("hash")
    data_check_string = '\n'.join('='.join(i) for i in sorted_data.items()).encode()
    secret_key = hmac.new(b"WebAppData", TELEGRAM_BOT_TOKEN.encode(), hashlib.sha256).digest()
    return hmac.new(secret_key, data_check_string, hashlib.sha256).hexdigest() == hash

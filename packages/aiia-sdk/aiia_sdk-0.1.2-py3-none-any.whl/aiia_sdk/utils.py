import hmac
import hashlib

def generate_signature(secret, message):
    return hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
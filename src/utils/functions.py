import hashlib

def hash_sha256(text: str) -> str:
    return hashlib.sha256(bytes(text, 'utf-8')).hexdigest()

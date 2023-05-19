import hashlib


def calculate_hash(value):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(value.encode('utf-8'))
    hashed_value = sha256_hash.hexdigest()
    return hashed_value
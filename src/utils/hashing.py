import hashlib

def hash_values(*values):
    raw = "|".join(map(str, values))
    return hashlib.sha256(raw.encode()).hexdigest()
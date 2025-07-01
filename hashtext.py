import hashlib
def hash_string(plaintext):
    return hashlib.sha256(plaintext.encode()).hexdigest()

def verify_hash(hash, plaintext):
    return hash_string(plaintext) == hash


if __name__ == "__main__":
    hash = hash_string("hello")
    print(hash)
    print(hash.hexdigest())

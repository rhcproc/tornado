
def get_nonce():
    import random
    return random.randrange(1,5)

def get_hash(raw_password):
    import hashlib
    import logging
    logging.warning(type(raw_password))
    hashed_pw = hashlib.sha256(raw_password.encode('utf-8'))
    return hashed_pw.hexdigest()[:20]
   

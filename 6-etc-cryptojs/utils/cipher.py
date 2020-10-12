
def insert_cipher_info(cipher):
    from pymongo import MongoClient
    client = MongoClient('localhost')
    db = client.test1
    tag = get_tag(16)
    db.cipher_info.insert(dict(cipher=cipher, tag=tag))
    client.close()
    return dict(cipher=cipher, tag=tag)

def get_cipher_info(tag):
    from pymongo import MongoClient
    client = MongoClient('localhost')
    db = client.test1
    data = None
    queries = db.cipher_info.find(dict(tag=tag))
    for query in queries : data = query
    client.close()
    return data

def get_tag(length):
    import random
    import string
    from pymongo import MongoClient
    client = MongoClient('localhost')
    db = client.test1
    tag = ''.join(random.choice(string.hexdigits) for i in range(length))
    tag_check = db.cipher_info.find(dict(tag=tag))
    data = None
    client.close()
    for check in tag_check : data = check
    if not data == None : get_nonce(length)
    else : return tag


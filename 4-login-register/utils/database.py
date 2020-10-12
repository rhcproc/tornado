
def insert_userinfo_to_db(username, password):
    from pymongo import MongoClient 
    client = MongoClient('localhost')
    db = client.testdb
    userinfo = None
    queries = db.userinfo.find(dict(username=username))
    for query in queries : userinfo = query
    client.close()
    if userinfo == None : 
        db.userinfo.insert(dict(username=username,
                                password=password))
        return True
    else : return False

def check_userinfo(username, password):
    from .cipher import get_hash
    from pymongo import MongoClient
    client = MongoClient('localhost')
    db = client.testdb

    hashed_pw = get_hash(password)
    queries = db.userinfo.find(dict(username=username))
    userinfo = None
    for query in queries : userinfo = query
    if userinfo == None : return False
    else :
        if userinfo['password'] == hashed_pw : 
            return True
        else : return False
    
def check_register_userinfo(username, password):
    from .cipher import get_hash
    from pymongo import MongoClient
    import logging
    logging.warning("%s|%s" %(username, password))
    client = MongoClient('localhost')
    db = client.testdb
    
    hashed_pw = get_hash(password)
    queries = db.userinfo.find(dict(username=username))
    userinfo = None
    for query in queries : userinfo = query
    if userinfo != None or password == "": return False
    else : return True

    
    


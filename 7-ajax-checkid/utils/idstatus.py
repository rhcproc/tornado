
def get_id_status(inputid):
    from pymongo import MongoClient
    client = MongoClient('localhost')
    db = client.testdb
    data, message = None, None 
    data = db.userinfo.find_one(dict(userid = inputid))
    if len(inputid) < 4: message = "- Minimum character is 4"
    elif len(inputid) > 20 : message = "- Maximum character is 20"
    elif data != None : message = "- ID '%s' exist" %inputid
    else : message = "- ID '%s' is possible" %inputid
    client.close()
    return message

def insert_id_to_db(inputid):
    from pymongo import MongoClient
    client = MongoClient('localhost')
    db = client.testdb
    db.userinfo.insert(dict(userid = inputid))
    client.close()
    return


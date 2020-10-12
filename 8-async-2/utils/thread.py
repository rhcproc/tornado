#-*- coding:utf-8 -*-

import pymongo
import _thread
import time
import logging
import random

db = pymongo.MongoClient('localhost').testdb

def start_thread():
    _thread.start_new_thread(main, ())

def main():
    time_counter = 0
    end_name = list(db.counter.find().sort("_id",-1).limit(1))
    main_name = None
    logging.warning(end_name)
    logging.warning(end_name)
    if len(end_name) == 0 : main_name = "M01"
    else :
        main_name = int(end_name[0]['name'].split("M")[1]) + 1
        main_name = "M"+str(main_name).zfill(2)
    r = lambda: random.randint(0,255)
    color = "#%02X%02X%02X" %(r(),r(),r())
    check = db.counter.insert(dict(name=main_name,
                                   counter=time_counter,
                                   color=color))
    
    while(1):
        time.sleep(1)
        time_counter += 1
        db.counter.update(dict(name=main_name), 
                         {"$set":dict(counter = time_counter)})
        if time_counter == 100 : break
                

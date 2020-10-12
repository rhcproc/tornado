

import sqlite3 as lite
import sys
import logging

class DatabaseHandler:
    def __init__(self):
        self.conn = None
        self.cur = None 

    def set_database(self, db_name):
        self.conn = lite.connect(db_name)        
        
    def create_table(self, table_name, types):
        query = "\
        create table if not exists {} ({})".format(table_name, types)
        self.cur = self.conn.cursor()
        try :
            self.cur.execute(query)
            return True
        except Exception as e :
            return False

    def insert_data(self, query, data_list): # data_list 
        self.cur = self.conn.cursor()

        try :
            self.cur.execute(query, data_list)
            self.conn.commit()
            return True
        except Exception as e : 
            return False
        

    def select_data(self, query):
        try :
            self.conn.row_factory = lite.Row
            self.cur = self.conn.cursor()
            self.cur.execute(query)
            rows = self.cur.fetchall()
            temp = []
            for row in rows: temp.append(dict(row))
            return temp
        except Exception as e:
            return False


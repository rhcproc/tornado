import tornado.web

from utils.cipher import *
from utils.database import *
from .base import BaseHandler

class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("register.html")

    def post(self):
        getusername = self.get_argument('username')
        getpassword = self.get_argument('password')
        check = check_register_userinfo(getusername, getpassword)
        if check == True : 
            hashed_pw = get_hash(getpassword)
            insert_check = insert_userinfo_to_db(getusername, hashed_pw)
            self.redirect("/")
        else : self.redirect("/register")
        
        

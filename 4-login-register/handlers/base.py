#-*- coding:utf-8 -*-

import tornado.web
from utils.database import *

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class LoginHandler(BaseHandler):
    def get(self):
        incorrect = self.get_secure_cookie("incorrect")
        if incorrect and int(incorrect) > 25 :
            self.write('<center>blocked</center>')
            return
        self.render('login.html')

    def post(self):
        getusername = self.get_argument('username')
        getpassword = self.get_argument('password')
        check = check_userinfo(getusername, getpassword)
        if check == True : 
            self.set_secure_cookie("user", self.get_argument("username"))
            self.set_secure_cookie("incorrect", "0")
            self.redirect(self.reverse_url("main"))
        else:
            incorrect = self.get_secure_cookie("incorrect")
            if not incorrect:
                incorrect = 0
            self.set_secure_cookie("incorrect", str(int(incorrect)+1))
            self.write('<center>something wrong with your data <a href="/">Go Home</a></center>')

class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", self.reverse_url("main")))


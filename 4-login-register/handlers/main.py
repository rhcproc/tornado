import tornado.web

from utils.cipher import *
from .base import BaseHandler

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("main.html",nonce = self.get_secure_cookie("user"))

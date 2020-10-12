#-*- coding:utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import logging

from tornado.options import define, options

from handlers.main import *
from handlers.base import *

define("port", default=3000, help="run on the given port", type=int)

def get_handler_list() :

    handler_list = [
        tornado.web.url(r'/', MainHandler, name="main"),
        tornado.web.url(r'/login', LoginHandler, name="login"),
        tornado.web.url(r'/logout', LogoutHandler, name="logout")
    ]
    return handler_list

class Application(tornado.web.Application):
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        handler_list = get_handler_list()
        settings = {
            'cookie_secret' : 'NN',
            'login_url' : '/login',
            'template_path' : os.path.join(base_dir, 'templates'),
            'static_path' : os.path.join(base_dir, 'static'),
            'debug' : True,
            'xsrf_cookies' : True,
        }
        tornado.web.Application.__init__(self, handlers=handler_list, **settings)

def main():
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    logging.warning("ID : demo, Password : deom")
    logging.warning("http://127.0.0.1:{}".format(options.port))
    main()

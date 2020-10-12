#-*- coding:utf -*-

import tornado.httpserver
import tornado.ioloop
import tornado.web
import os.path
import motor
import json
import logging 

from operator import itemgetter
from tornado import gen
from tornado.options import define, options
import utils.thread

define("port", default=3000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        settings = {
            'cookie_secret' : 'A231EJRJ213OEJWNE',
            'login_url' : '/login',
            'template_path' : os.path.join(base_dir, 'templates'),
            'static_path' : os.path.join(base_dir, 'static'),
            'debug' : True, 
            'xsrf_cookies' : False,
        }
        tornado.web.Application.__init__(self, [
            tornado.web.url(r"/", MainHandler, name="main"),
        ],  **settings)
        self.db = motor.MotorClient('localhost').testdb

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

class MainHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        self.render("index.html")

    @gen.coroutine
    def post(self):
        getkey = tornado.escape.json_decode(self.request.body)
        logging.warning(getkey)
        if getkey['key'] == "counter" : utils.thread.start_thread()
        cursor = self.db.counter.find({},{'_id':False}).sort([('name',-1)])
        while (yield cursor.fetch_next):
            self.write(json.dumps(cursor.next_object()))
        self.finish()

def main():
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

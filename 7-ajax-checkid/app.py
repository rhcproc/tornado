#-*- coding:utf-8 -*-
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import json

from utils.idstatus import *
from tornado.options import define, options

define("port", default=3000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/idstatus", IdStatusHandler),
        ]
        settings = dict(
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static")
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages=None)
    
    def post(self):
        inputid = self.get_argument('currentid')
        check = insert_id_to_db(inputid)
        self.redirect("/")

class IdStatusHandler(tornado.web.RequestHandler):
    def post(self):
        jsonobj = tornado.escape.json_decode(self.request.body)
        inputid = jsonobj['inputid'].strip()
        message = get_id_status(inputid)
        response_to_send = dict(message = message)
        self.write(json.dumps(response_to_send))

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    print ("Open http://127.0.0.1:{}".format(options.port))
    main()

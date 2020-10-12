#!/usr/bin/env python
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path

import json
import datetime

from tornado.options import define, options

define("port", default=3000, help="run on the given port", type=int)
cl = []
cl2 = []
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/second", SecondHandler),
            (r"/api1",Api1Handler),
            (r"/ws1", Socket1Handler),
            (r"/api2",Api2Handler),
            (r"/ws2", Socket2Handler),
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

class SecondHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("second.html", messages=None)

class Socket1Handler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    def open(self):
        if self not in cl : cl.append(self)
    def on_close(self):
        if self in cl : cl.remove(self)

class Socket2Handler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    def open(self):
        if self not in cl2 : cl2.append(self)
    def on_close(self):
        if self in cl2 : cl2.remove(self)

class Api1Handler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, *args):
        self.finish()
        id = self.get_argument("id")
        value = self.get_argument("value")
        data = {"id":id, "value":value}
        data = json.dumps(data)
        for c in cl : c.write_message(data)

class Api2Handler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, *args):
        self.finish()
        id = self.get_argument("id")
        value = self.get_argument("value")
        data = {"id":id, "value":value}
        data = json.dumps(data)
        for c in cl2 : c.write_message(data)

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    print ("Open http://127.0.0.1:{}".format(options.port))
    main()


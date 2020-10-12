#-*- coding:utf-8 -*-

import tornado.web
import tornado.httpserver
import tornado.ioloop
import os.path

from tornado.options import define, options

define("port", default=3000, help="run on the given port", type=int)

def add(x,y):
    return x+y

class Application(tornado.web.Application):
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        settings = {
            "template_path":os.path.join(base_dir, "templates"),
            "static_path":os.path.join(base_dir, "static"),
            "debug":True,
        }
        tornado.web.Application.__init__(self, [
            tornado.web.url(r"/(favicon.ico)", tornado.web.StaticFileHandler, {"path":""}), 
            tornado.web.url(r"/", MainHandler, name="main"),
        ], **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        ivalue = "normal_value_1"
        ilist = ["list_value_1","list_value_2","list_value_3"]
        idict = dict(a="dict_value_1", b="dict_value_2")
        ilistdict = [dict(number=1),dict(number=2), dict(number=3)]
        
        self.render("index.html", ivalue = ivalue,
                                  ilist = ilist,
                                  idict = idict,
                                  ilistdict = ilistdict,
                                  add = add)
def main():
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    print ("Open http://127.0.0.1:{}".format(options.port))
    main()


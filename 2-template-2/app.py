#-*- coding:utf-8 -*-
import tornado.web
import tornado.httpserver
import tornado.ioloop
import os.path
import logging

from tornado.options import define, options

define("port", default=3000, help="run on the given port", type=int)

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
            tornado.web.url(r"/second", SecondHandler, name="secode"),
        ], **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        linkify_test = "<b> http://localhost:3000/second </b>"
        students = [dict(name="abc"), dict(name="def"), dict(name="ghi")]
        self.render("base.html", students=students, title="title",
                                 linkify_test = linkify_test)

class SecondHandler(tornado.web.RequestHandler):
    def get(self):
        linkify_test = "http://localhost:3000"
        students = [dict(name="abc"), dict(name="def"), dict(name="ghi")]
        self.render("bold.html", students=students, title="title",
                                linkify_test = linkify_test)

def main():
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    logging.warning("Open http://127.0.0.1:{}".format(options.port))
    main()


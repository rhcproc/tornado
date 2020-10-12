#-*- coding:utf-8 -*-

import tornado.web
import tornado.httpserver
import tornado.ioloop
import os.path

from tornado.options import define, options

define("port", default=3000, help="run on the given port", type=int)

def get_picture_list():
    import os
    path = os.path.dirname( os.path.abspath( __file__ ))
    picture_list = list()
    
    for picture_name in os.listdir(path+"/static/pictures/"):
        picture_list.append(dict(picture_name=picture_name))
    return picture_list

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
        #picture_list = utils.picture_manager.get_picture_list()
        picture_list = get_picture_list()
        self.render("index.html", picture_list = picture_list)

    def post(self):
        if self.request.files:
            picture = self.request.files['picture'][0]
            fp = open("static/pictures/"+picture["filename"], "wb")
            fp.write(picture["body"])
            fp.close()
        else : pass
        self.redirect("/")

def main():
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    print ("Open http://127.0.0.1:{}".format(options.port))
    main()


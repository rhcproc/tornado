#-*- coding:utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import handlers

from tornado.options import define, options

define("port", default=3000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        handler_list = handlers.get_handler_list
        settings = {
            'cookie_secret' : '2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ',
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
    print("Open http://127.0.0.1:{}".format(options.port))
    main()


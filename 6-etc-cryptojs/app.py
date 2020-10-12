#-*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.escape
import os.path
import logging

import utils.cipher 
from tornado.options import define, options

define("port", default=3000, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        cipher = data['cipher']
        logging.warning(cipher)
        cipher_info = utils.cipher.insert_cipher_info(cipher)
        logging.warning(cipher_info)
        self.write(cipher_info['tag'])

class TagHandler(tornado.web.RequestHandler):
    def get(self, tag):
        cipher_info = utils.cipher.get_cipher_info(tag)
        logging.warning(cipher_info)
        if cipher_info == None : self.write("Error")
        self.render('tag.html', cipher_info = cipher_info)

class Application(tornado.web.Application):
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        settings = {
            'template_path': os.path.join(base_dir, 'templates'),
            'static_path': os.path.join(base_dir, 'static'),
            'debug':True,
        }
        
        tornado.web.Application.__init__(self, [
            tornado.web.url(r'/', MainHandler, name='main'),
            tornado.web.url(r'/tag/([^/]+)', TagHandler, name='tag'),
        ], **settings)

def main():
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    print ("Open http://127.0.0.1:{}".format(options.port))
    main()


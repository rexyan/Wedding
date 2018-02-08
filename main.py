# --coding:utf-8--
import tornado.ioloop
import tornado.web
import settings
import sys
import urls
from tornado.netutil import bind_sockets
from tornado.httpserver import HTTPServer


if __name__ == "__main__":
    if len(sys.argv) > 1:
        MAIN_SITE_PORT = int(sys.argv[1])
    else:
        MAIN_SITE_PORT = settings.SITE_PORT
    app = tornado.web.Application(urls.url, **settings.project_setting)
    sockets = bind_sockets(MAIN_SITE_PORT)
    server = HTTPServer(app, xheaders=True)
    server.add_sockets(sockets)
    print ('Tornado server started on port %s.' % MAIN_SITE_PORT)
    tornado.ioloop.IOLoop.instance().start()
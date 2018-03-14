# --coding:utf-8--
import tornado.ioloop
import tornado.web
import tornado.locale
import settings
import sys
import urls
from tornado.netutil import bind_sockets
from tornado.httpserver import HTTPServer
import os

if __name__ == "__main__":
    if len(sys.argv) > 1:
        MAIN_SITE_PORT = int(sys.argv[1])
    else:
        MAIN_SITE_PORT = settings.SITE_PORT
    app = tornado.web.Application(urls.url, **settings.project_setting)
    i18n_path = os.path.join(os.path.dirname(__file__), 'translations')
    tornado.locale.load_translations(i18n_path)
    tornado.locale.set_default_locale('zh_CN')
    sockets = bind_sockets(MAIN_SITE_PORT)
    server = HTTPServer(app, xheaders=True)
    server.add_sockets(sockets)
    print ('Tornado server started on port %s.' % MAIN_SITE_PORT)
    tornado.ioloop.IOLoop.instance().start()
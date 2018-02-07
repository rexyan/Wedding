# --coding:utf-8--

import tornado
from views.base import BaseHandler
import settings
import os
import time
import io

class AdminIndexHandler(BaseHandler):
    def get(self):
        self.render('admin_login.html')

class AdminGoodsHandler(BaseHandler):
    def get(self):
        self.render('admin_goods.html')

class AdminUserHandler(BaseHandler):
    def get(self):
        self.render('admin_user.html')
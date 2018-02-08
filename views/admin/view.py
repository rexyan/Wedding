# --coding:utf-8--

import tornado
from views.base import BaseHandler
import settings
import os
import time
import io
from click.decorators import argument

# 后台首页
class AdminIndexHandler(BaseHandler):
    def get(self):
        self.render('admin_login.html')

# 商品
class AdminGoodsIndexHandler(BaseHandler):
    def get(self):
        self.render('admin_goods.html')
        
class AdminGoodsAddHandler(BaseHandler):
    def get(self):
        self.render('admin_goods_add.html')

class AdminGoodsHandler(BaseHandler):
    def get(self, argument):
        pass
        
    def post(self):
        pass
    
    def delete(self):
        pass
    
    def patch(self):
        pass
        

# 用户
class AdminUserIndexHandler(BaseHandler):
    def get(self):
        self.render('admin_user.html')
        
class AdminUserAddHandler(BaseHandler):
    def get(self):
        self.render('admin_user_add.html')

class AdminUserHandler(BaseHandler):
    def get(self, argument):
        pass
        
    def post(self):
        pass
    
    def delete(self):
        pass
    
    def patch(self):
        pass

# Layout模版      
class AdminLayoutHandler(BaseHandler):
    def get(self):
        self.render('admin_layout.html')

        
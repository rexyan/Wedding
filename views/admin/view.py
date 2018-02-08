# --coding:utf-8--

from views.base import BaseHandler
from models.Base import session

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
        data = {}
        data['username'] = self.get_argument('username', None)
        data['password'] = self.get_argument('password', None)
        data['user_realname'] = self.get_argument('user_realname', None)
        data['user_email'] = self.get_argument('user_email', None)
        data['sex'] = self.get_argument('sex', None)
        data['age'] = self.get_argument('age', None)
        data['init_point'] = self.get_argument('init_point', '0')
        data['vip'] = self.get_argument('vip', '1')
        session.execute("")
        session.commit()


    def delete(self):
        pass
    
    def patch(self):
        pass

# Layout模版      
class AdminLayoutHandler(BaseHandler):
    def get(self):
        self.render('admin_layout.html')

# 工具
class UtilsHandler(BaseHandler):
    def get(self):
        pass
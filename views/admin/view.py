# --coding:utf-8--
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from views.base import BaseHandler
from models.Base import session
from models.User import Users
from models.ProductType import ProductType
import json
from utils.auth import sec_pass

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


# 商品类型
class AdminGoodsTypeIndexHandler(BaseHandler):
    def get(self):
        self.render('admin_goods_type.html')


class AdminGoodsTypeAddHandler(BaseHandler):
    def get(self):
        self.render('admin_goods_type_add.html')


class AdminGoodsTypeHandler(BaseHandler):
    def get(self, argument):
        pass

    def post(self):
        # 新增商品类型
        try:
            # 获取前端传来的参数
            data = json.loads(self.get_argument('data'))
            session.add(ProductType(**data))
            session.commit()
        except:
            # 事务
            session.rollback()
            self.write_json("faild", code=0)
        finally:
            session.close()
        self.write_json("success", code=1)

    def delete(self):
        pass

    def patch(self):
        pass

# 用户
class AdminUserIndexHandler(BaseHandler):
    def get(self):
        # 用户列表页面
        ret = session.query(Users)[0:10]
        self.render('admin_user.html', user_data=ret)

class AdminUserAddHandler(BaseHandler):
    def get(self):
        # 添加用户页面
        self.render('admin_user_add.html')

class AdminUserHandler(BaseHandler):
    # 查询用户, argument为传来的参数
    def get(self, argument):
        ret = session.query(Users).filter_by(UserID=argument).first()
        self.write_json(data=ret.to_json(), code=1)

    def post(self):
        # 新增用户
        try:
            # 获取前端传来的参数
            data = json.loads(self.get_argument('data'))
            # 保存访问IP
            data['UserLastVisitIP'] = self.request.remote_ip
            # 密码加密
            data['UserPwd'] = sec_pass(data['UserPwd'])
            session.add(Users(**data))
            session.commit()
        except:
            # 事务
            session.rollback()
            self.write_json("faild", code=0)
        finally:
            session.close()
        self.write_json("success", code=1)


    def delete(self, argument):
        try:
            session.query(Users).filter(Users.UserID == argument).delete()
            self.write_json("success", code=1)
        except Exception,e:
            self.write_json("faild", code=0)

    
    def patch(self, argument):
        updata_json = json.loads(self.get_argument('data'))
        try:
            session.query(Users).filter(Users.UserID == argument).update(updata_json)
            session.commit()
            self.write_json("success", code=1)
        except Exception, e:
            print e
            self.write_json("faild", code=0)


# Layout模版      
class AdminLayoutHandler(BaseHandler):
    def get(self):
        self.render('admin_layout.html')

# 工具
class UtilsHandler(BaseHandler):
    def get(self):
        pass
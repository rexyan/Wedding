# --coding:utf-8--
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
from views.base import BaseHandler
from models.Base import session, noautoflushsession
from models.User import Users
from models.ProductType import ProductType
from models.Product import Product
from models.Order import Order
from models.Comment import Comment
from models.Manager import Manager
from models.LoginMap import LoginMap
import json
from utils.auth import sec_pass
from utils import up_qiniu
import requests
import settings
import datetime
from utils import redis_queue_send_email
import random


# 后台首页
class AdminIndexHandler(BaseHandler):
    def get(self):
        self.session.set('UserSession', "")
        self.render('admin_login.html')

# 商品
class AdminProductIndexHandler(BaseHandler):
    # 获取商品列表
    def get(self):
        ret = noautoflushsession.query(Product)
        for i, x in enumerate(ret):
            # 根据ProductTypeID查询每个类型的名称【有个坑，需要关闭sqlalchemy自动刷新】
            q_name = ""
            q_name = noautoflushsession.query(ProductType).filter_by(ProductTypeID=x.ProductType).first()
            if q_name:
                q_name = q_name.ProductTypeName
            ret[i].ProductType = q_name
        noautoflushsession.close()
        self.render('admin_product.html', Product_list=ret)
        
class AdminProductAddHandler(BaseHandler):
    def get(self):
        self.render('admin_product_add.html')
# 商品
class AdminProductHandler(BaseHandler):
    def get(self, argument):
        print "argument", argument
        if argument == 'All':
            data_list = []
            ret = session.query(ProductType)
            for x in ret:
                data_list.append(x.to_json())
            self.write_json(data=data_list)
        else:
            ret = session.query(Product).filter_by(ProductID=argument).first()
            data_list = ret.to_json()
            self.write_json(data=data_list, code=1)
    def post(self):
        # 新增商品
        try:
            # 获取前端传来的参数
            data = json.loads(self.get_argument('data'))
            if data['IsHot'] == '1':
                data['IsHot'] = True
            else:
                data['IsHot'] = False
            if data['IsNew'] == '1':
                data['IsNew'] = True
            else:
                data['IsNew'] = False
            pro = Product(**data)
            session.add(pro)
            session.commit()
            self.write_json(pro.ProductID, code=1)
        except Exception,e :
            # 事务
            print e
            session.rollback()
            self.write_json("failed", code=0)
        finally:
            session.close()
    
    def delete(self, argument):
        try:
            noautoflushsession.query(Product).filter(Product.ProductID == int(argument)).delete()
            noautoflushsession.commit()
            noautoflushsession.close()
            self.write_json("success", code=1)
        except Exception, e:
            print e
            self.write_json("failed", code=0)
    
    def patch(self, argument):
        updata_json = json.loads(self.get_argument('data'))
        print updata_json
        try:
            if updata_json['IsNew'] == '1':
                updata_json['IsNew'] = True
            else:
                updata_json['IsNew'] = False

            if updata_json['IsHot'] == '1':
                updata_json['IsHot'] = True
            else:
                updata_json['IsHot'] = False

            updata_json['ProductType'] = int(updata_json['ProductType'])
            updata_json['ProductMarketPrice'] = int(updata_json['ProductMarketPrice'])
            updata_json['ProductFavorablePrice'] = int(updata_json['ProductFavorablePrice'])
            updata_json['ProductVipPrice'] = int(updata_json['ProductVipPrice'])
            updata_json['ProductPoint'] = int(updata_json['ProductPoint'])
            updata_json['ProductCount'] = int(updata_json['ProductCount'])

            session.query(Product).filter(Product.ProductID == argument).update(updata_json)
            session.commit()
            self.write_json("success", code=1)
        except Exception, e:
            print e
            self.write_json("failed", code=0)


# 商品类型
class AdminProductTypeIndexHandler(BaseHandler):
    def get(self):
        ret = session.query(ProductType).all()
        self.render('admin_product_type.html', product_type = ret)
class AdminProductTypeAddHandler(BaseHandler):
    def get(self):
        self.render('admin_product_type_add.html')
class AdminProductTypeHandler(BaseHandler):
    def get(self, argument):
        pass
    def post(self):
        # 新增商品类型
        try:
            # 获取前端传来的参数
            data = json.loads(self.get_argument('data'))
            session.add(ProductType(**data))
            session.commit()
            self.write_json("success", code=1)
        except:
            # 事务
            session.rollback()
            self.write_json("failed", code=0)
        finally:
            session.close()
    def delete(self, argument):
        try:
            session.query(ProductType).filter(ProductType.ProductTypeID == argument).delete()
            self.write_json("success", code=1)
        except Exception, e:
            self.write_json("failed", code=0)
    def patch(self, argument):
        updata_json = json.loads(self.get_argument('data'))
        try:
            session.query(ProductType).filter(ProductType.ProductTypeID == argument).update(updata_json)
            session.commit()
            self.write_json("success", code=1)
        except Exception, e:
            print e
            self.write_json("failed", code=0)

# 用户
class AdminUserIndexHandler(BaseHandler):
    def get(self):
        # 用户列表页面# get post
        ret = session.query(Users)[0:10]  # 10  2  5
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
            self.write_json("success", code=1)
        except:
            # 事务
            session.rollback()
            self.write_json("failed", code=0)
        finally:
            session.close()
    def delete(self, argument):
        try:
            session.query(Users).filter(Users.UserID == argument).delete()
            self.write_json("success", code=1)
            session.commit()
        except Exception,e:
            self.write_json("failed", code=0)
    def patch(self, argument):
        updata_json = json.loads(self.get_argument('data'))
        try:
            session.query(Users).filter(Users.UserID == argument).update(updata_json)
            session.commit()
            self.write_json("success", code=1)
        except Exception, e:
            print e
            self.write_json("failed", code=0)

# 上传图片
class AdminProductImgesIndexHandler(BaseHandler):
    # 上传图片页面
    def get(self):
        self.render('admin_product_image.html')

    # 上传图片接口
    def post(self):
        pid = self.get_argument('pid')
        try:
            complete_file_path = None
            file_name = None
            return_save_file_path = os.path.join('images', 'upload') # 要保存到数据库的地址
            save_file_path = os.path.join('static', return_save_file_path)
            if self.get_argument('image_type')=='1':
                # 小图地址字段
                image_type = 'ProductSmallPicture'
                # 上传到哪儿
                upload_type = 'SmallPictureUpType'
            else:
                # 大图地址字段
                image_type = 'ProductBigPictureProductBigPicture'
                # 上传到哪儿
                upload_type = 'BigPictureUpType'

            if self.get_argument('save_type') == '2' or self.get_argument('save_type') == '3':
                # 七牛云、又拍云
                save_file_path = os.path.join('static', return_save_file_path)

            # 将文件先保存到本地
            file_metas = self.request.files["file"]  # 获取上传文件信息
            for meta in file_metas:  # 循环文件信息
                file_name = meta['filename']  # 获取文件的名称
                # 拼接完整目录
                complete_file_path = os.path.join(save_file_path, file_name)
                with open(complete_file_path, 'wb') as up:  # os拼接文件保存路径，以字节码模式打开
                    up.write(meta['body'])  # 将文件写入到保存路径目录

            # 要保存到数据库的文件名
            return_save_file_path = file_name

            # 是否上传七牛云
            if self.get_argument('save_type') == '2':
                # 上传
                obj = up_qiniu.QINIU()
                # 返回七牛地址
                return_save_file_path = obj.upload(complete_file_path, file_name)

            # 是否上传又拍云
            if self.get_argument('save_type') == '3':
                pass
                # 上传
                # 返回七牛地址
                # return_save_file_path

            # 入库
            session.query(Product).filter(Product.ProductID == pid).update({image_type: return_save_file_path, upload_type:int(self.get_argument('save_type'))})
            session.commit()
            session.close()
            self.write_json("success", code=1)
        except Exception, e:
            print e
            self.write_json("failed", code=0)

# 订单
class AdminOrderFalseHandler(BaseHandler):
    def get(self):
        ret = session.query(Order).filter_by(OrderStatus=False).all()
        self.render('admin_order.html', order_list=ret)

class AdminOrderTrueHandler(BaseHandler):
    def get(self):
        ret = session.query(Order).filter_by(OrderStatus=True).all()
        self.render('admin_order1.html', order_list=ret)

class AdminOrderHandler(BaseHandler):
    def get(self, argument):
        ret = session.query(Order).filter_by(OrderID=argument).first()
        self.write_json(data=ret.to_json(), code=1)

    def patch(self, argument):
        updata_json = json.loads(self.get_argument('data'))
        try:
            if updata_json['OrderStatus'] == '1':
                updata_json['OrderStatus'] = True
            else:
                updata_json['OrderStatus'] = False
            session.query(Order).filter(Order.OrderID == argument).update(updata_json)
            session.commit()
            self.write_json("success", code=1)
        except Exception, e:
            print e
            self.write_json("failed", code=0)

# 评论
class AdminCommentIndexHandler(BaseHandler):
    def get(self):
        ret = session.query(Comment)[0:10]
        self.render('admin_comment.html', comment_list=ret)

class AdminCommenHandler(BaseHandler):
    def get(self, argument):
        ret = session.query(Comment).filter_by(CommentID=argument).first()
        self.write_json(data=ret.to_json(), code=1)

    def patch(self, argument):
        updata_json = json.loads(self.get_argument('data'))
        try:
            if updata_json['Status'] == '1':
                updata_json['Status'] = True
            else:
                updata_json['Status'] = False
            session.query(Comment).filter(Comment.CommentID == argument).update(updata_json)
            session.commit()
            self.write_json("success", code=1)
        except Exception, e:
            print e
            self.write_json("failed", code=0)

    def delete(self, argument):
        try:
            session.query(Comment).filter(Comment.CommentID == argument).delete()
            self.write_json("success", code=1)
        except Exception, e:
            self.write_json("failed", code=0)

# 后台登录
class AdminUserLoginHandler(BaseHandler):
    def get(self):
        if self.session.get('UserSession'):
            managername = self.session['UserSession'].get('ManagerName')
            code = 1
        else:
            managername = ""
            code = 0
        self.write_json(managername, code=code)

    def post(self):
        # 验证luosimao
        code = 1
        msg = "success"
        data_json = json.loads(self.get_argument('data'))
        luosimao_rep = data_json.get('luosimao_rep')
        check_json = {
            'api_key':settings.LUOSIMAO_API_KEY,
            'response':luosimao_rep
        }
        check_response = requests.post(settings.LUOSIMAO_CHECK_ADDRESS, data=check_json)
        if json.loads(check_response.content).get('res') != 'success':
            code = 0
            msg = u"人机验证失败"
        # 验证帐号密码
        ret = session.query(Manager).filter(Manager.ManagerName == data_json.get('user_email'),
                                            Manager.ManagerPsd == sec_pass(data_json.get('user_pass'))).first()
        if not ret:
            code = 0
            msg = u"帐号密码不正确"
        else:
            # 设置session
            self.session.set('UserSession', ret.to_json())
            # 更新信息
            update_json = {
                'ManagerLastVisitTime': datetime.datetime.now(),
                'ManagerLastVisitIP': self.request.remote_ip
            }
            session.query(Manager).filter(Manager.ManagerName == data_json.get('user_email')).update(update_json)
        self.write_json(msg, code=code)


# Layout模版      
class AdminLayoutHandler(BaseHandler):
    def get(self):
        self.render('admin_layout.html')

# 工具
class UtilsHandler(BaseHandler):
    def get(self):
        pass

# 发送邮件
class SendEmailHandler(BaseHandler):
    def post(self, argument):
        if argument == '1':
            # 账户激活邮件
            data_json = json.loads(self.get_argument('data'))
            to_email = data_json.get('email')
            self.session['bind_email'] = to_email
            obj = redis_queue_send_email.REDIS_QUEUE()
            random_str = str(random.randint(1, 99999))
            self.session['email_random'] = random_str
            content1 = '你本次在'+settings.WEB_NAME+"的验证码为:<a>" + str(random_str)+"</a>"
            content = '''
<html>
<body>
<p>亲爱的用户：</p>
<pre>
您收到这封邮件，是由于在 有缘婚恋网 进行了邮箱验证，使用了这个邮箱地址。
如果您并没有访问过 有缘婚恋网，或没有进行上述操作，请忽 略这封邮件。您不需要退订或进行其他进一步的操作。
</pre>
<pre>
===============验证码===================

''' + content1 + '''

            </pre>
            </body>
            </html>
            '''

            obj.send_email_via_queue(settings.SMTP_USER, to_email, settings.WEB_NAME+"验证", content)
            self.write_json("验证码发送成功", code=1)
            # print "argument", argument


class CheckCodeHandler(BaseHandler):
    def post(self, argument):
        if argument == '1':
            data_json = json.loads(self.get_argument('data'))
            code = data_json.get('code')
            if self.session['email_random'] == code:

                # 新增到User表
                user_data = {"UserName": self.session['nickname'], "UserEmail": self.session['bind_email'], "UserLastVisitIP": self.request.remote_ip}
                user_obj = Users(**user_data)
                session.add(user_obj)
                session.commit()
                # 添加到映射表
                data = {"OpenID": self.session['openid'], "UserID": str(user_obj.UserID)}
                session.add(LoginMap(**data))
                self.session.set('index_user', user_obj)
                session.commit()
                session.close()
                print "user_data", user_data
                # self.session['index_user'] = user_data
                self.write_json("验证成功", code=1)
            else:
                self.write_json("验证失败", code=0)
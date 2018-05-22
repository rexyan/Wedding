# --coding:utf-8--
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
from views.base import BaseHandler
from models.Base import session, noautoflushsession
from models.Product import Product
from models.ProductType import ProductType
from models.ShopCart import ShopCart
from models.LoginMap import LoginMap
from models.User import Users
from models.Collection import Collection
from models.DeliveryAddress import DeliveryAddress
from models.Order import Order
from models.Comment import Comment
import settings
import requests
import json
from utils.auth import sec_pass
from utils import redis_queue_send_email
import time
from views.view_utils.tools import getAllProductType
from views.view_utils.tools import getProductTypeByPid
from views.view_utils.tools import getProductByPidFirst
from views.view_utils.tools import getRecommendProduct
from views.view_utils.tools import getComLast3Limit
from views.view_utils.tools import getAllProductType_EN
from pay.alipay.main import return_order_string
from sqlalchemy.sql import func
import datetime
from sqlalchemy import or_


class IndexHandler(BaseHandler):
    def get(self):
        pid = self.get_argument('pid', None)
        # product_type = session.query(ProductType).all()
        product_type = getAllProductType()
        product_type_list = [x.to_json() for x in product_type]
        if pid:
            # banner上的文字
            name = None
            for x in product_type_list:
                if str(x['ProductTypeID']) == pid:
                    name = x['ProductTypeName']

            # 获取品牌分类
            # pid_product_list = session.query(Product).filter(Product.ProductType == pid).all()
            pid_product_list = getProductTypeByPid(pid)
            product_brand_list = [x.to_json() for x in pid_product_list][:5]

            # 排序方式
            order = self.get_argument('order', "")
            if order:
                def sorted_func(s):
                    if order == '2':
                        col = "ProductMarketPrice"
                    elif order == '3':
                        col = "ProductMarketPrice"
                    elif order == '4':
                        col = "ProductCollectNum"
                    elif order == '5':
                        col = "ProductOnTime"
                    elif order == '6':
                        col = "ProductBuyNum"
                    else:
                        col = "ProductID"
                    return s.to_json()[col]
                pid_product_list = sorted(pid_product_list, key=sorted_func, reverse=True)

            # 获取标签、关键字
            key_words_list = [x.to_json()['ProductKeywords'] for x in pid_product_list][:8]

            # 查询最高价
            max_price = session.query(func.max(Product.ProductMarketPrice)).first()[0]

            # 获取推荐的商品
            hot_product_list = [x.to_json() for x in pid_product_list if x.to_json()['IsHot']==1][:4]

            # 商品列表、分页
            data_count = len(pid_product_list)  # 数据总条数
            page_num = int(self.get_argument('page', 0))
            every_page_num = end_page_num = 12
            max_page, remainder = divmod(data_count, every_page_num)
            if remainder != 0:
                max_page += 1
            start_page_num = 0
            if page_num != 0:
                start_page_num = (page_num-1) * every_page_num
                end_page_num = (page_num) * every_page_num
            # 筛选价格区间
            filter_price = int(self.get_argument('filter_price', 0))
            if filter_price:
                pid_product_list = [x for x in pid_product_list if x.ProductMarketPrice < filter_price][start_page_num:end_page_num]

            # 筛选商品品牌
            brand = self.get_argument('brand', "")
            brand = json.loads('"' + "".join([(i and "\\" + i) for i in brand.split('%')]) + '"')
            if brand:
                pid_product_list = [x for x in pid_product_list if x.ProductBrand == brand][start_page_num:end_page_num]

            # 筛选标签
            label = self.get_argument('label', "")
            print "=====", [(i and "\\" + i) for i in label.split('%')]
            label = json.loads('"' + "".join([(i and "\\" + i) for i in label.split('%')]) + '"')
            print "label", label
            if label:
                pid_product_list = [x for x in pid_product_list if x.ProductKeywords == label][start_page_num:end_page_num]
            pid_product_list = [x.to_json() for x in pid_product_list][start_page_num:end_page_num]
            page_data_count = len(pid_product_list) # 返回前台的数据总条数
            page_info = {"pid": pid, "max_page": max_page, "data_count": data_count, "page_data_count": page_data_count, "page_num": page_num}
            self.render(
                'index_shop_list.html',
                name=name,
                product_brand_list=product_brand_list,
                key_words_list=key_words_list,
                max_price=max_price,
                hot_product_list=hot_product_list,
                product_list=pid_product_list,
                page_info=page_info,
            )
        else:
            # 获取首页大图下的三个图（是新品且是热门）
            info_1 = session.query(Product).filter(Product.IsHot == 1, Product.IsNew == 1)[0:3]
            # 获取首页下的5个热门商品
            info_2 = session.query(Product).filter(Product.IsHot == 1, Product.IsNew == 0)[0:4]
            info_3 = session.query(Product).filter(Product.IsHot == 0, Product.IsNew == 1)[0:4]

            # 获取评论的商品，取最新三条
            # comment_product_limit_3 = session.query(Comment).filter_by(Status=True).all()[-4:-1]
            comment_product_limit_3 = getComLast3Limit()
            comment_product_limit_3_list = []
            for com in comment_product_limit_3:
                rmp_com_dict = com.to_json()
                product_id = rmp_com_dict['ProductID']
                product = getProductByPidFirst(product_id).to_json()
                rmp_com_dict['product'] = product
                comment_product_limit_3_list.append(rmp_com_dict)
            self.render(
                'index_index.html',
                info_1=info_1,
                info_2=info_2,
                info_3=info_3,
                comment_product_limit_3_list=comment_product_limit_3_list
            )

# 登录页
class IndexLoginHandler(BaseHandler):
    def get(self):
        self.render('index_login.html')

    def post(self):
        data = json.loads(self.get_argument('data'))
        luosimao_rep = data.get('luosimao_rep')
        check_json = {
            'api_key': settings.LUOSIMAO_API_KEY,
            'response': luosimao_rep
        }
        check_response = requests.post(settings.LUOSIMAO_CHECK_ADDRESS, data=check_json)
        if json.loads(check_response.content).get('res') != 'success':
            code = 3
            msg = u"人机验证失败"
            self.write_json(msg, code=code)
            return

        # 验证帐号密码，帐号状态
        ret = session.query(Users).filter(Users.UserEmail ==data.get('Email'), Users.UserPwd == sec_pass(data.get('Pass'))).first()
        if not ret:
            code = 2
            msg = u"帐号密码错误"
            self.write_json(msg, code=code)
            return
        if ret.UserHashCode:
            # 账户未激活
            code = 0
            msg = u"帐号未激活"
            self.write_json(msg, code=code)
            return
        else:
            code = 1
            msg = u"登录成功"
            session.query(Users).filter(Users.UserID == ret.UserID).update({"UserLastVisitTime":datetime.datetime.now(),"UserLastVisitIP":self.request.remote_ip})
            self.session['index_user'] = ret
            session.commit()
            self.write_json(msg, code=code)

    def patch(self):
        self.session['index_user'] = ""
        self.write_json(u"注销成功", code=1)

# 注册页
class IndexRegisterHandler(BaseHandler):
    def get(self):
        self.render('index_register.html')

    def post(self):
        # 注册
        try:
            # 获取前端传来的参数
            data = json.loads(self.get_argument('data'))

            luosimao_rep = data.get('luosimao_rep')
            check_json = {
                'api_key': settings.LUOSIMAO_API_KEY,
                'response': luosimao_rep
            }
            check_response = requests.post(settings.LUOSIMAO_CHECK_ADDRESS, data=check_json)
            if json.loads(check_response.content).get('res') != 'success':
                code = 3
                msg = u"人机验证失败"
                self.write_json(msg, code=code)
                return
            data.pop('luosimao_rep')
            data['UserAge'] = int(data['UserAge'])
            data['UserPwd'] = sec_pass(data['UserPwd'])
            data['UserLastVisitIP'] = self.request.remote_ip
            active_hash_code = sec_pass(str(int(time.time())))
            data['UserHashCode'] = active_hash_code
            session.add(Users(**data))
            session.commit()
            active_url = '<a href='+'http://'+settings.WEB_DOMAIN_NAME+\
                         '/active_email/?address='+data['UserEmail']+\
                         '&hash_code='+active_hash_code+'>http://'+settings.WEB_DOMAIN_NAME+\
                         '/active_email/?address='+data['UserEmail']+\
                         '&hash_code='+active_hash_code+'</a>'
            content = '''
<html>
<body>
<p>亲爱的用户：</p>
<pre>
  您收到这封邮件，是由于在 春色撩人网站 进行了新用户注册，或用户修改 Email 使用 了这个邮箱地址。
 如果您并没有访问过 春色撩人网站，或没有进行上述操作，请忽 略这封邮件。您不需要退订或进行其他进一步的操作。
</pre>
<pre>
 ===============激活链接===================

'''+ active_url +'''

(如果上面不是链接形式，请将该地址手工粘贴到浏览器地址栏再访问)

</pre>
</body>
</html>
'''
            obj = redis_queue_send_email.REDIS_QUEUE()
            obj.send_email_via_queue(settings.SMTP_USER, data['UserEmail'], settings.WEB_NAME + "注册", content)

            self.write_json("success", code=1)
        except Exception,e:
            # 事务
            session.rollback()
            self.write_json("failed", code=0)
        finally:
            session.close()

# 模版页
class IndexLayoutHandler(BaseHandler):
    def get(self):
        self.render('index_layout.html')

# QQ登录页
class IndexQQLoginPageHandler(BaseHandler):
    def get(self):
        self.render('qq.html')

class IndexQQLoginHandler(BaseHandler):
    def get(self):
        try:
            # 获取code
            code = self.get_argument('code')
            # 根据code获取access_token
            url1 = 'https://graph.qq.com/oauth2.0/token?grant_type=authorization_code&client_id='+settings.QQ_APP_ID+'&client_secret='\
                   +settings.QQ_APPKey+'&code='+code+'&redirect_uri='+settings.QQ_CollBackUrl
            req1 = requests.get(url1)
            access_token = req1.content.split('&')[0].split('=')[1]
            # 根据access_token获取openid
            url2 = 'https://graph.qq.com/oauth2.0/me?access_token='+access_token
            req2 = requests.get(url2)
            openid = json.loads(req2.content.split('(')[1].split(')')[0]).get('openid')

            # 根据openid获取用户信息
            url3 = 'https://graph.qq.com/user/get_user_info?access_token='+access_token+'&oauth_consumer_key='+settings.QQ_APP_ID+'&openid='+openid
            req3 = requests.get(url3)
            qq_user_info = json.loads(req3.content)
            nickname = qq_user_info.get('nickname')

            # 查询有没有绑定帐号
            self.session['openid'] = openid
            self.session['nickname'] = nickname
            ret = session.query(LoginMap).filter_by(OpenID=openid).first()
            if not ret:
                self.redirect('/register/?status=1')  # 未绑定帐号
            else:
                # 登录
                userid = ret.UserID
                ret = session.query(Users).filter_by(UserID=userid).first()
                self.session['index_user'] = ret
                session.query(Users).filter(Users.UserID == ret.UserID).update({
                    "UserLastVisitTime": datetime.datetime.now(),
                    "UserLastVisitIP": self.request.remote_ip})
                session.commit()
                self.redirect('/index')
        except Exception,e:
            self.redirect('/register/?status=2')  # 第三方登录出现错误

class WeiboLoginHandler(BaseHandler):
    def get(self):
        code = self.get_argument('code')
        url = 'https://api.weibo.com/oauth2/access_token'
        url1 = 'https://api.weibo.com/2/users/show.json'
        canshu = {
            "client_id":"1816247821",
            "client_secret":"eda276ef28ae911ba030fea6bfbbc360",
            "grant_type":"authorization_code",
            "code":code,
            "redirect_uri":"http://test.com/check_weibo/"
        }
        re = requests.post(url, data=canshu)
        re_json = json.loads(re.content)
        re1 = requests.get(url1 + "?access_token=" + re_json.get('access_token') + "&uid=" + re_json.get('uid'))
        weibo_user_info = json.loads(re1.content)

        ret = session.query(LoginMap).filter_by(OpenID=weibo_user_info.get('id')).first()
        if not ret:
            self.session['openid'] = weibo_user_info.get('id')
            self.session['nickname'] = weibo_user_info.get('screen_name')
            self.redirect('/register/?status=1')  # 未绑定帐号
        else:
            # 登录
            userid = ret.UserID
            ret = session.query(Users).filter_by(UserID=userid).first()
            session.query(Users).filter(Users.UserID == ret.UserID).update({"UserLastVisitTime": datetime.datetime.now(),
                                                                            "UserLastVisitIP": self.request.remote_ip})
            self.session['index_user'] = ret
            session.commit()
            self.redirect('/index')


class ActiveEmailHandler(BaseHandler):
    def get(self):
        try:
            email_address = self.get_argument('address')
            hash_code = self.get_argument('hash_code')
            ret = session.query(Users).filter_by(UserEmail=email_address).first()
            if ret and hash_code == ret.UserHashCode:
                # 激活账户
                session.query(Users).filter(Users.UserEmail==email_address).update({"UserHashCode": ""})
                session.commit()
                self.redirect('/login/?active_status=1')
        except Exception, e :
            self.redirect('/login/?active_status=0')

class CheckLoginHandler(BaseHandler):
    def get(self):
        try:
            user_info = self.session['index_user'].to_json()
            code = 1
        except Exception, e:
            user_info = None
            code = 0
        finally:
            self.write_json(user_info, code=code)

class GetProductListHandler(BaseHandler):
    def get(self):
        _ = self.locale.translate
        ret_list = getAllProductType_EN()
        # ret_list = ret_list = session.query(ProductType).all()
        all_list = []
        for ret in ret_list:
            tmp_json = ret.to_json()
            tmp_json['ProductTypeName'] = _(tmp_json['ProductTypeName'])  # js中不能进行国际化，只好放在后端翻译
            all_list.append(tmp_json)
        self.write_json(all_list, code=1)

class BaiduMapHandler(BaseHandler):
    def get(self):
        self.render('baidu_map.html')

class CollectionProductHandler(BaseHandler):
    def post(self, argument):
        # 收藏商品
        try:
            user_info = self.session['index_user'].to_json()
            ret = session.query(Collection).filter(Collection.UserID == user_info.get('UserID'), Collection.ProductID == argument).first()
            if ret:
                code = 0
                msg = u"该商品已经收藏了"
            else:
                code = 1
                msg = u"收藏成功"
                data = {"UserID": user_info.get('UserID'), "ProductID": argument}
                session.add(Collection(**data))
                session.commit()
        except Exception, e:
            print e
            code = 3
            msg = u"用户未登录"
        finally:
            self.write_json(msg, code=code)


class ShopCartHandler(BaseHandler):
    def get(self):
        user_info = self.session['index_user'].to_json()
        result = []
        ret = session.query(ShopCart).filter(ShopCart.UserID == user_info.get('UserID')).all()
        for x in ret:
            current_product_info = session.query(Product).filter_by(ProductID=x.ProductID).first().to_json()
            current_product_info['BuyNum'] = x.BuyNum
            current_product_info['ShopCartID'] = x.ShopCartID
            result.append(current_product_info)
        self.render('index_shopcart.html', shopcart_list=result)


class AddShopCartHandler(BaseHandler):
    def post(self, argument):
        try:
            user_info = self.session['index_user'].to_json()
            buy_num = 1
            arg_data = self.get_argument('data')
            if arg_data and arg_data!="":
                argument_data = json.loads(self.get_argument('data'))
                buy_num = argument_data.get('buy_num')

            # 查询购物车中是否已经有该商品
            ret = session.query(ShopCart).filter(ShopCart.UserID == user_info.get('UserID'),
                                                 ShopCart.ProductID == argument).first()
            if ret:
                session.query(ShopCart).filter(ShopCart.UserID == user_info.get('UserID'),
                                               ShopCart.ProductID == argument).update({"BuyNum": int(buy_num)+int(ret.BuyNum)})
            else:
                if buy_num:
                    data = {"UserID": user_info.get('UserID'), "ProductID": argument, "BuyNum":buy_num}
                else:
                    data = {"UserID": user_info.get('UserID'), "ProductID": argument}
                session.add(ShopCart(**data))
            session.commit()
            code = 1
            msg = u"添加购物车成功"
        except Exception, e:
            code = 0
            msg= u"添加购物车出错"
        finally:
            self.write_json(msg, code=code)

    def patch(self, cartid):
        number = json.loads(self.get_argument('data')).get('number')
        session.query(ShopCart).filter(ShopCart.ShopCartID == cartid).update({"BuyNum": number})
        session.commit()
        self.write_json(u"购物车更新成功", code=1)

    def delete(self, cartid):
        try:
            session.query(ShopCart).filter(ShopCart.ShopCartID == cartid).delete()
            session.commit()
            self.write_json("success", code=1)
        except Exception, e:
            self.write_json("failed", code=0)

class DeliveryAddressHandler(BaseHandler):
    def get(self):
        try:
            result_list = []
            user_info = self.session['index_user'].to_json()
            ret = session.query(DeliveryAddress).filter_by(UserID=user_info.get('UserID')).all()
            code =1
            for x in ret:
                result_list.append(x.to_json())
            data = result_list
        except Exception,e:
            code = 0
            data = u"收货地址获取失败"
        finally:
            self.write_json(data, code=1)

class AlipayHandler(BaseHandler):
    def get(self):
        user_info = self.session['index_user'].to_json()
        data = json.loads(self.get_argument('data'))
        trade_no = sec_pass(str(int(time.time()))) # 交易号
        # 加入订单
        save_data = {"TRADE_NO": trade_no, "UserID": user_info.get('UserID'),
                     "OrderTotalPrice": data.get('totalprice'),
                     "OrderPayType": 1,
                     "OrderStatus":False,
                     "OrderSendAddress": data.get('address')}
        try:
            product_list = []
            for i, x in enumerate(data.get('all_data')):
                # 删除购物车信息
                session.query(ShopCart).filter(ShopCart.ShopCartID == x['shopcartid']).delete()
                # 修改商品信息
                session.query(Product).filter(Product.ProductID == x['productid']).update({"ProductBuyNum": Product.ProductBuyNum + int(x['num'])})
                product_list.append(str(x['productid']))
            save_data['ProductID'] = ','.join(product_list)
            session.add(Order(**save_data))
            session.commit()
        except Exception, e:
            session.rollback()
        # 接受支付参数,整理支付宝接口所需参数
        order_string = return_order_string(u'春色撩人支付测试', trade_no, int(data.get('totalprice')),settings.ALIPAY_RETURN_URL)
        self.redirect(settings.ALIPAY_GETWAY + "?" + order_string)

    def post(self):
        pass


class AlipaySusscessHandler(BaseHandler):
    def get(self):
        # 支付成功，改变订单状态
        user_info = self.session['index_user'].to_json()
        out_trade_no = self.get_argument('out_trade_no', None)
        if out_trade_no:
            select_order_status = session.query(Order).filter_by(TRADE_NO=out_trade_no).first()
            if not select_order_status.OrderStatus:
                session.query(Order).filter(Order.TRADE_NO == out_trade_no).update({"OrderStatus": True})
                session.commit()
                # 发送邮件
                content = '''
<html>
<body>
<p>亲爱的用户：</p>
<pre>
您已经成功购买商品。我们已经收到您的订单 <a>'''+out_trade_no+'''</a> 的购买请求，商品正在发货中,请等待！
如果您并没有访问过 有缘婚恋网，或没有进行上述操作，请忽 略这封邮件。您不需要退订或进行其他进一步的操作。
</pre>
<pre>

</pre>
</body>
</html>
'''
                obj = redis_queue_send_email.REDIS_QUEUE()
                obj.send_email_via_queue(settings.SMTP_USER, user_info.get('UserEmail'), settings.WEB_NAME + "订单信息", content)
        order_list = session.query(Order).filter_by(UserID=user_info.get('UserID')).all()
        all_data = []
        for i, x in enumerate(order_list):
            ProductID = x.to_json().get('ProductID')
            product_info_list = []
            for id in ProductID.split(','):
                print "==========", id
                ProductInfo = session.query(Product).filter_by(ProductID=id).first().to_json()
                product_info_list.append(ProductInfo)
            all_data.append({"order": x.to_json(), "product_info": product_info_list})
        self.render('order_list.html', order_list=all_data)

    def post(self):
        pass


class ErrorHandler(BaseHandler):
    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('404.html')
        elif status_code == 500:
            self.render('500.html')
        else:
            self.write('error:' + str(status_code))

class ShopProductDetailHandler(BaseHandler):
    def get(self):
        pid = self.get_argument('pid', None)
        ProductInfo = []
        comment_list = []
        comment_msg = ""
        comment_count = 0
        if pid:
            ProductInfo = getProductByPidFirst(pid).to_json()
            try:
                suer_info = self.session['index_user'].to_json()
                order_info = session.query(Order).filter(Order.UserID == suer_info['UserID'], Order.ProductID == pid).first()
                if not order_info:
                    comment_msg = u'未购买过该商品，不能进行评论'
            except Exception, e:
                comment_msg = u'未登录、登录后才能进行相关操作'
            comment = session.query(Comment).filter(Comment.ProductID == pid, Comment.Status==True).all()
            for com in comment:
                com_dict = com.to_json()
                UserID = int(com_dict['UserID'])
                try:
                    UserName= session.query(Users).filter_by(UserID=UserID).first().to_json()['UserName']
                    com_dict['UserName'] = UserName
                except:
                    com_dict['UserName'] = u"有缘网用户"
                comment_list.append(com_dict)
            comment_count = len(comment_list)

            # 商品详情下的推荐
            # recommend_product = session.query(Users).all()[-8:-1]
            recommend_product = getRecommendProduct()
        self.render('index_shop_detail.html', ProductInfo=ProductInfo, comment_list=comment_list,
                    comment_msg=comment_msg, comment_count=comment_count, recommend_product=recommend_product)


class ProductCommentHandler(BaseHandler):
    def post(self):
        arg_data = json.loads(self.get_argument('data'))
        user_info = self.session['index_user'].to_json()
        data = {"UserID":user_info['UserID'], "ProductID":arg_data['pid'], "Content":arg_data['user_comment_content'], "Status":False}
        obj = Comment(**data)
        session.add(obj)
        session.commit()
        self.write_json(u"新增成功、审核成功后即可显示！", code=1)

class UserCenterHandler(BaseHandler):
    def get(self):
        user_info = self.session['index_user'].to_json()
        self.render('index_user_center.html', user_info=user_info)

    def post(self):
        try:
            data = json.loads(self.get_argument('data'))
            if data.keys()[0] == "UserSex":
                data['UserSex'] = 1 if data['UserSex'] == u"男" else 0
            user_info = self.session['index_user'].to_json()
            session.query(Users).filter(Users.UserID == user_info['UserID']).update(data)
            user_info = session.query(Users).filter_by(UserID=user_info['UserID']).first()
            self.session['index_user'] = user_info
            self.write_json(u"修改成功", code=1)
            session.commit()
        except Exception, e:
            print e
            self.write_json(u"修改失败", code=0)


class ProductHistoryHandler(BaseHandler):
    def get(self):
        user_info = self.session['index_user'].to_json()
        history_list = session.query(Order).filter_by(UserID=user_info['UserID']).all()
        self.render('index_product_history_list.html', history_list=history_list)

class WishListHandler(BaseHandler):
    def get(self):
        user_info = self.session['index_user'].to_json()
        wish_list = []
        try:
            wish_all = session.query(Collection).filter_by(UserID=user_info['UserID']).all()
            for wish in wish_all:
                wish_dict = wish.to_json()
                Product = getProductByPidFirst(wish_dict['ProductID'])
                wish_dict['product'] = Product.to_json()
                wish_list.append(wish_dict)
        except Exception,e:
            print e
            pass

        self.render('index_wish_list.html', wish_list=wish_list)

    def post(self):
        user_info = self.session['index_user'].to_json()
        pid = self.get_argument('pid')
        session.query(Collection).filter(Collection.ProductID == pid, Collection.UserID==user_info['UserID']).delete()
        session.commit()
        self.write_json(u"移除成功", code=1)


class MyAddressHandler(BaseHandler):
    def get(self):
        user_info = self.session['index_user'].to_json()
        my_address = session.query(DeliveryAddress).filter_by(UserID=user_info['UserID']).all()
        self.render('my_address.html', my_address=my_address)

    def post(self):
        data = json.loads(self.get_argument('data'))
        user_id = self.session['index_user'].to_json()['UserID']
        data["UserID"] = user_id
        obj = DeliveryAddress(**data)
        session.add(obj)
        session.commit()
        self.write_json(u"新增成功", code=1)

    def delete(self, argument):
        try:
            noautoflushsession.query(DeliveryAddress).filter(DeliveryAddress.DeliveryAddressID == int(argument)).delete()
            noautoflushsession.commit()
            noautoflushsession.close()
            self.write_json("success", code=1)
        except Exception, e:
            print e
            self.write_json("failed", code=0)


class SearchHandler(BaseHandler):
    def get(self):
        search_info = self.get_argument('info')
        words = [u'%'+x+'%' for x in search_info.split('-')]
        product_search_result = []
        rule = or_(*[Product.ProductName.like(w) for w in words])
        product_search_result.extend(session.query(Product).filter(rule).all())
        rule = or_(*[Product.ProductBrand.like(w) for w in words])
        product_search_result.extend(session.query(Product).filter(rule).all())
        product_search_result = [x.to_json() for x in product_search_result]
        self.render('search_list.html', product_search_result=product_search_result)

    def post(self):
        pass


class AddressPageHandler(BaseHandler):
    def get(self):
        self.render('address.html')
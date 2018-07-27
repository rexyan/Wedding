# --*--coding:utf-8--*--
import json
from views.base import BaseHandler
from models.Base import session
from views.order.model import Order
from views.comment.model import Comment
from views.product.utils import get_product_by_pid_first
from views.user.model import Users
from views.comment.utils import get_recommend_product
from views.shopcard.model import ShopCart
from views.product.model import Product


class ShopProductDetailHandler(BaseHandler):
    def get(self):
        pid = self.get_argument('pid', None)
        productinfo = []
        comment_list = []
        comment_msg = ""
        comment_count = 0
        recommend_product = ''
        if pid:
            productinfo = get_product_by_pid_first(pid).to_json()
            try:
                suer_info = self.session['index_user'].to_json()
                order_info = session.query(Order).filter(Order.UserID == suer_info['UserID'],
                                                         Order.ProductID == pid).first()
                if not order_info:
                    comment_msg = u'未购买过该商品，不能进行评论'
            except Exception, e:
                print(e)
                comment_msg = u'未登录、登录后才能进行相关操作'
            comment = session.query(Comment).filter(Comment.ProductID == pid, Comment.Status == True).all()
            for com in comment:
                com_dict = com.to_json()
                userid = int(com_dict['UserID'])
                try:
                    username = session.query(Users).filter_by(UserID=userid).first().to_json()['UserName']
                    com_dict['UserName'] = username
                except Exception, e:
                    print(e)
                    com_dict['UserName'] = u"有缘网用户"
                comment_list.append(com_dict)
            comment_count = len(comment_list)

            # 商品详情下的推荐
            # recommend_product = session.query(Users).all()[-8:-1]
            recommend_product = get_recommend_product()
        self.render('index_shop_detail.html', ProductInfo=productinfo, comment_list=comment_list,
                    comment_msg=comment_msg, comment_count=comment_count, recommend_product=recommend_product)


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
        msg = ''
        code = ''
        try:
            user_info = self.session['index_user'].to_json()
            buy_num = 1
            arg_data = self.get_argument('data')
            if arg_data and arg_data != "":
                argument_data = json.loads(self.get_argument('data'))
                buy_num = argument_data.get('buy_num')

            # 查询购物车中是否已经有该商品
            ret = session.query(ShopCart).filter(ShopCart.UserID == user_info.get('UserID'),
                                                 ShopCart.ProductID == argument).first()
            if ret:
                session.query(ShopCart).filter(ShopCart.UserID == user_info.get('UserID'),
                                               ShopCart.ProductID == argument).update(
                    {"BuyNum": int(buy_num) + int(ret.BuyNum)})
            else:
                if buy_num:
                    data = {"UserID": user_info.get('UserID'), "ProductID": argument, "BuyNum": buy_num}
                else:
                    data = {"UserID": user_info.get('UserID'), "ProductID": argument}
                session.add(ShopCart(**data))
            session.commit()
            code = 1
            msg = u"添加购物车成功"
        except Exception, e:
            print(e)
            code = 0
            msg = u"添加购物车出错"
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
            print(e)
            self.write_json("failed", code=0)

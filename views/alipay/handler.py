# --coding:utf-8--*--
import settings
import time
import json
from views.order.model import Order
from utils.auth import sec_pass
from models.Base import session
from views.base import BaseHandler
from pay.alipay.main import return_order_string
from views.product.model import Product
from views.shopcard.model import ShopCart
from views.email import utils as redis_queue_send_email


class AlipayHandler(BaseHandler):
    def get(self):
        user_info = self.session['index_user'].to_json()
        data = json.loads(self.get_argument('data'))
        trade_no = sec_pass(str(int(time.time())))  # 交易号
        # 加入订单
        save_data = {"TRADE_NO": trade_no, "UserID": user_info.get('UserID'),
                     "OrderTotalPrice": data.get('totalprice'),
                     "OrderPayType": 1,
                     "OrderStatus": False,
                     "OrderSendAddress": data.get('address')}
        try:
            product_list = []
            for i, x in enumerate(data.get('all_data')):
                # 删除购物车信息
                session.query(ShopCart).filter(ShopCart.ShopCartID == x['shopcartid']).delete()
                # 修改商品信息
                session.query(Product).filter(Product.ProductID == x['productid']).update(
                    {"ProductBuyNum": Product.ProductBuyNum + int(x['num'])})
                product_list.append(str(x['productid']))
            save_data['ProductID'] = ','.join(product_list)
            session.add(Order(**save_data))
            session.commit()
        except Exception, e:
            print(e)
            session.rollback()
        # 接受支付参数,整理支付宝接口所需参数
        order_string = return_order_string(u'春色撩人支付测试', trade_no, int(data.get('totalprice')),
                                           settings.ALIPAY_RETURN_URL)
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
                content = u'''
<html>
<body>
<p>亲爱的用户：</p>
<pre>
您已经成功购买商品。我们已经收到您的订单 <a>''' + out_trade_no + u'''</a> 的购买请求，商品正在发货中,请等待！
如果您并没有访问过 有缘婚恋网，或没有进行上述操作，请忽 略这封邮件。您不需要退订或进行其他进一步的操作。
</pre>
<pre>

</pre>
</body>
</html>
'''
                obj = redis_queue_send_email.REDIS_QUEUE()
                obj.send_email_via_queue(settings.SMTP_USER, user_info.get('UserEmail'), settings.WEB_NAME + u"订单信息",
                                         content)
        order_list = session.query(Order).filter_by(UserID=user_info.get('UserID')).all()
        all_data = []
        for i, x in enumerate(order_list):
            productid = x.to_json().get('ProductID')
            product_info_list = []
            for pid in productid.split(','):
                productinfo = session.query(Product).filter_by(ProductID=pid).first().to_json()
                product_info_list.append(productinfo)
            all_data.append({"order": x.to_json(), "product_info": product_info_list})
        self.render('order_list.html', order_list=all_data)

    def post(self):
        pass

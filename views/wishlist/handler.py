# --*--coding:utf8--*--
from views.base import BaseHandler
from models.Base import session
from views.collection.model import Collection
from views.product.utils import get_product_by_pid_first


class WishListHandler(BaseHandler):
    def get(self):
        user_info = self.session['index_user'].to_json()
        wish_list = []
        try:
            wish_all = session.query(Collection).filter_by(UserID=user_info['UserID']).all()
            for wish in wish_all:
                wish_dict = wish.to_json()
                product = get_product_by_pid_first(wish_dict['ProductID'])
                wish_dict['product'] = product.to_json()
                wish_list.append(wish_dict)
        except Exception, e:
            print e
            pass

        self.render('index_wish_list.html', wish_list=wish_list)

    def post(self):
        user_info = self.session['index_user'].to_json()
        pid = self.get_argument('pid')
        session.query(Collection).filter(Collection.ProductID == pid, Collection.UserID == user_info['UserID']).delete()
        session.commit()
        self.write_json(u"移除成功", code=1)

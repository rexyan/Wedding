from views.base import BaseHandler
from models.Base import session
from views.order.model import Order
from views.product.utils import get_all_product_type_en


class ProductHistoryHandler(BaseHandler):
    def get(self):
        user_info = self.session['index_user'].to_json()
        history_list = session.query(Order).filter_by(UserID=user_info['UserID']).all()
        self.render('index_product_history_list.html', history_list=history_list)


class GetProductListHandler(BaseHandler):
    def get(self):
        _ = self.locale.translate
        ret_list = get_all_product_type_en()
        # ret_list = ret_list = session.query(ProductType).all()
        all_list = []
        for ret in ret_list:
            tmp_json = ret.to_json()
            tmp_json['ProductTypeName'] = _(tmp_json['ProductTypeName'])  # js中不能进行国际化，只好放在后端翻译
            all_list.append(tmp_json)
        self.write_json(all_list, code=1)

from views.base import BaseHandler
from models.Base import session
from views.order.model import Order


class ProductHistoryHandler(BaseHandler):
    def get(self):
        user_info = self.session['index_user'].to_json()
        history_list = session.query(Order).filter_by(UserID=user_info['UserID']).all()
        self.render('index_product_history_list.html', history_list=history_list)

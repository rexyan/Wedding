from views.base import BaseHandler
from models.Base import session
from sqlalchemy import or_
from views.product.model import Product


class SearchHandler(BaseHandler):
    def get(self):
        search_info = self.get_argument('info')
        words = [u'%' + x + '%' for x in search_info.split('-')]
        product_search_result = []
        rule = or_(*[Product.ProductName.like(w) for w in words])
        product_search_result.extend(session.query(Product).filter(rule).all())
        rule = or_(*[Product.ProductBrand.like(w) for w in words])
        product_search_result.extend(session.query(Product).filter(rule).all())
        product_search_result = [x.to_json() for x in product_search_result]
        self.render('search_list.html', product_search_result=product_search_result)

    def post(self):
        pass

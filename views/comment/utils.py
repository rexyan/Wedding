# --*--coding:utf-8--*--
from views.product.model import Product
from views.comment.model import Comment
from models.Base import session
from views.view_utils.memcached_cache import memorize


@memorize
def get_recommend_product():
    recommendproduct = session.query(Product).all()[-16:-1]
    result = [x.to_json() for x in recommendproduct]
    return result


@memorize
def get_com_last_3_limit():
    return session.query(Comment).filter_by(Status=True).all()[-4:-1]

# --*--coding:utf-8--*--
from models.ProductType import ProductType
from models.Product import Product
from models.Comment import Comment
from models.Base import session
from views.view_utils.memcached_cache import memorize


# Python 装饰器
@memorize
def get_all_product_type():
    ret_list = session.query(ProductType).all()
    return ret_list


@memorize
def get_all_product_type_en():
    ret_list = session.query(ProductType).all()
    return ret_list


@memorize
def get_product_type_by_pid(pid):
    product = session.query(Product).filter(Product.ProductType == pid).all()
    return product


@memorize
def get_product_by_pid_first(pid):
    product = session.query(Product).filter(Product.ProductID == pid).first()
    return product


@memorize
def get_recommend_product():
    RecommendProduct = session.query(Product).all()[-16:-1]
    result = [x.to_json() for x in RecommendProduct]
    return result


@memorize
def get_com_last_3_limit():
    return session.query(Comment).filter_by(Status=True).all()[-4:-1]

from models.ProductType import ProductType
from model import Product
from models.Base import session
from views.view_utils.memcached_cache import memorize


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

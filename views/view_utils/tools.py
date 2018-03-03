#--*--coding:utf-8--*--

from models.ProductType import ProductType
from models.Product import Product
from models.Base import session, noautoflushsession
from views.view_utils.memcached_cache import memorize

#Python 装饰器
@memorize
def getAllProductType():
    ret_list = session.query(ProductType).all()
    return ret_list

@memorize
def getProductTypeByPid(pid):
    ProductType = session.query(Product).filter(Product.ProductType == pid).all()
    return ProductType

# 获取导航  --  发起ajax请求 -- 装饰器 --- 如果redis中有  --  直接返回  --- 如果没有 -- 查询数据库  -- 放进缓存
#--*--coding:utf-8--*--

from models.ProductType import ProductType
from models.Product import Product
from models.Comment import Comment
from models.Base import session, noautoflushsession
from views.view_utils.memcached_cache import memorize

#Python 装饰器
@memorize
def getAllProductType():
    ret_list = session.query(ProductType).all()
    return ret_list

@memorize
def getAllProductType_EN():
    ret_list = session.query(ProductType).all()
    return ret_list

@memorize
def getProductTypeByPid(pid):
    product = session.query(Product).filter(Product.ProductType == pid).all()
    return product

@memorize
def getProductByPidFirst(pid):
    product = session.query(Product).filter(Product.ProductID == pid).first()
    return product

@memorize
def getRecommendProduct():
    RecommendProduct = session.query(Product).all()[-16:-1]
    result = [x.to_json() for x in RecommendProduct]
    return result

@memorize
def getComLast3Limit():
    return session.query(Comment).filter_by(Status=True).all()[-4:-1]

# 获取导航  --  发起ajax请求 -- 装饰器 --- 如果redis中有  --  直接返回  --- 如果没有 -- 查询数据库  -- 放进缓存
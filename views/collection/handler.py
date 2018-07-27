# --*--coding:utf8--*--
from views.base import BaseHandler
from models.Base import session
from views.collection.model import Collection


class CollectionProductHandler(BaseHandler):
    def post(self, argument):
        msg = None
        code = None
        # 收藏商品
        try:
            user_info = self.session['index_user'].to_json()
            ret = session.query(Collection).filter(Collection.UserID == user_info.get('UserID'),
                                                   Collection.ProductID == argument).first()
            if ret:
                code = 0
                msg = u"该商品已经收藏了"
            else:
                code = 1
                msg = u"收藏成功"
                data = {"UserID": user_info.get('UserID'), "ProductID": argument}
                session.add(Collection(**data))
                session.commit()
        except Exception, e:
            print e
            code = 3
            msg = u"用户未登录"
        finally:
            self.write_json(msg, code=code)

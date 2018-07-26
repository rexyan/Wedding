# --*--coding:utf8--*--
from views.base import BaseHandler
from models.Base import session
from model import Comment


class ProductCommentHandler(BaseHandler):
    def post(self):
        arg_data = json.loads(self.get_argument('data'))
        user_info = self.session['index_user'].to_json()
        data = {"UserID": user_info['UserID'], "ProductID": arg_data['pid'],
                "Content": arg_data['user_comment_content'], "Status": False}
        obj = Comment(**data)
        session.add(obj)
        session.commit()
        self.write_json(u"新增成功、审核成功后即可显示！", code=1)

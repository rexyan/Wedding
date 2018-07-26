# --*--coding:utf8--*--
from views.base import BaseHandler
from models.Base import session
import json
from model import Users


class UserCenterHandler(BaseHandler):
    def get(self):
        user_info = self.session['index_user'].to_json()
        self.render('index_user_center.html', user_info=user_info)

    def post(self):
        try:
            data = json.loads(self.get_argument('data'))
            if data.keys()[0] == "UserSex":
                data['UserSex'] = 1 if data['UserSex'] == u"男" else 0
            user_info = self.session['index_user'].to_json()
            session.query(Users).filter(Users.UserID == user_info['UserID']).update(data)
            user_info = session.query(Users).filter_by(UserID=user_info['UserID']).first()
            self.session['index_user'] = user_info
            self.write_json(u"修改成功", code=1)
            session.commit()
        except Exception, e:
            print e
            self.write_json(u"修改失败", code=0)

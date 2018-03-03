import tornado
from pycket.session import SessionMixin
import json
from utils.encode import MyEncoder


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    # def get_current_user(self):
    #     if not hasattr(self, '_user'):
    #         session_id = self.get_cookie('PYCKET_ID')
    #         try:
    #             user_id = self.session.get(session_id, '')['id']
    #         except:
    #             return None
    #         self._user = auth.get_user(user_id).to_dict()
    #     return self._user

    def write_json(self, data, status=200, code=0, type=True):
        ''''''
        self.set_status(status)
        data = {
            'code': code,
            'data': data
        }
        if type:
            self.write(json.dumps(data, indent=2, cls=MyEncoder))
        else:
            self.write(data)

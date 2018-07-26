# --coding:utf-8--*--
from views.base import BaseHandler
from models.Base import session, noautoflushsession
from model import DeliveryAddress
import json


class MyAddressHandler(BaseHandler):
    def get(self):
        user_info = self.session['index_user'].to_json()
        my_address = session.query(DeliveryAddress).filter_by(UserID=user_info['UserID']).all()
        self.render('my_address.html', my_address=my_address)

    def post(self):
        data = json.loads(self.get_argument('data'))
        user_id = self.session['index_user'].to_json()['UserID']
        data["UserID"] = user_id
        obj = DeliveryAddress(**data)
        session.add(obj)
        session.commit()
        self.write_json(u"新增成功", code=1)

    def delete(self, argument):
        try:
            noautoflushsession.query(DeliveryAddress).filter(
                DeliveryAddress.DeliveryAddressID == int(argument)).delete()
            noautoflushsession.commit()
            noautoflushsession.close()
            self.write_json("success", code=1)
        except Exception, e:
            print e
            self.write_json("failed", code=0)


class AddressPageHandler(BaseHandler):
    def get(self):
        self.render('address.html')

#--*--coding:utf-8--*--
import User
import Manager
from Base import session, noautoflushsession
import md5

class INIT_DEFAULT_USER(object):
    def __init__(self):
        pass

    def create_user(self):
        data = {"UserName": "default", "UserPwd": "b9d9b8ddd5e59bc8cac074a2272dfb28", "UserEmail": "default@test.com", "UserHashCode": ""}
        obj = User.Users(**data)
        session.add(obj)
        session.commit()

    def crete_manager(self):
        data = {"ManagerName": "superadmin", "ManagerPsd": "b9d9b8ddd5e59bc8cac074a2272dfb28"}
        obj = Manager.Manager(**data)
        session.add(obj)
        session.commit()

    def __del__(self):
        pass

if __name__=='__main__':
    obj = INIT_DEFAULT_USER()
    obj.create_user()
    obj.crete_manager()
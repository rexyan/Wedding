# --*--coding:utf8--*--
from Base import *
import datetime


# 创建单表
class LoginMap(Base):
    __tablename__ = 'loginmap'  # 表名
    MapID = Column(Integer, primary_key=True, autoincrement=True)
    OpenID = Column(String(100), unique=True, index=True)
    UserID = Column(String(100), unique=True, index=True)

    def __repr__(self):
        return "%s-%s" % (self.MapID, self.OpenID)

    def to_json(self):
        return {
            'MapID': self.MapID,
            'OpenID': self.OpenID,
            'UserID': self.UserID
        }


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


def main(arg):
    if arg == 1:
        init_db()
    elif arg == 0:
        drop_db()


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    main(1)


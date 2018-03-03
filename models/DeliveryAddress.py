# --*--coding:utf8--*--
from Base import *
import datetime


# 创建单表
class DeliveryAddress(Base):
    __tablename__ = 'deliveryaddress'  # 表名
    DeliveryAddressID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, index=True)
    UserProvince = Column(String(100))
    UserCity = Column(String(100))
    UserZipCode = Column(String(100))
    UserTelphone = Column(String(100))
    UserMobile = Column(String(100))
    ConsigneeName = Column(String(100))
    DetaileAddress = Column(String(100))

    def __repr__(self):
        return "%s-%s" % (self.DeliveryAddressID, self.DetaileAddress)

    def to_json(self):
        return {
            'DeliveryAddressID': self.DeliveryAddressID,
            'UserID': self.UserID,
            'UserProvince': self.UserProvince,
            'UserCity': self.UserCity,
            'UserZipCode': self.UserZipCode,
            'UserTelphone': self.UserTelphone,
            'UserMobile': self.UserMobile,
            'ConsigneeName': self.ConsigneeName,
            'DetaileAddress': self.DetaileAddress,
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


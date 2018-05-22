# --*--coding:utf8--*--
from Base import *
import datetime

ALIPAY = 1
WECHAT = 2
OTHER = 3
PAY_TYPE = {
    (ALIPAY, u"支付宝"),
    (WECHAT, u"微信"),
    (OTHER, u"其他集成支付")
}

# 创建单表
class Order(Base):
    __tablename__ = 'order'  # 表名
    OrderID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer)
    ProductID = Column(String(100))
    OrderTotalPrice = Column(String(100))
    OrderPayType = Column(Integer, default=OTHER)
    OrderStatus = Column(Boolean, default=False)
    OrderSendAddress = Column(String(1000))
    TRADE_NO = Column(String(100))

    def __repr__(self):
        return "%s-%s" % (self.OrderID, self.UserID)

    def to_json(self):
        return {
            'OrderID': self.OrderID,
            'UserID': self.UserID,
            'OrderTotalPrice': self.OrderTotalPrice,
            'OrderPayType': self.OrderPayType,
            'OrderStatus': self.OrderStatus,
            'OrderSendAddress': self.OrderSendAddress,
            'TRADE_NO': self.TRADE_NO,
            'ProductID': self.ProductID
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


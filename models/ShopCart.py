# --*--coding:utf8--*--
from Base import *
import datetime


# 创建单表
class ShopCart(Base):
    __tablename__ = 'shopcart'  # 表名
    ShopCartID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, index=True)
    ProductID = Column(Integer, index=True)
    BuyNum = Column(Integer, default=1)


    def __repr__(self):
        return "%s-%s" % (self.ShopCartID, self.UserID)

    def to_json(self):
        return {
            'ShopCartID': self.ShopCartID,
            'UserID': self.UserID,
            'ProductID': self.ProductID,
            'BuyNum': self.BuyNum,
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


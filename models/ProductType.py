# --*--coding:utf8--*--
from Base import *
import datetime


# 创建单表
class ProductType(Base):
    __tablename__ = 'product_type'  # 表名
    ProductTypeID = Column(Integer, primary_key=True, autoincrement=True)
    ProductTypeName = Column(String(100), unique=True, index=True)

    def __repr__(self):
        return "%s-%s" % (self.ProductTypeID, self.ProductTypeName)

    def to_json(self):
        return {
            'ProductTypeID': self.ProductTypeID,
            'ProductTypeName': self.ProductTypeName
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


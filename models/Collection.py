# --*--coding:utf8--*--
from Base import *
import datetime


# 创建单表
class Collection(Base):
    __tablename__ = 'collection'  # 表名
    CollectionID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, index=True)
    ProductID = Column(Integer, index=True)
    CollectTime = Column(DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return "%s-%s" % (self.ProductID, self.UserID)

    def to_json(self):
        return {
            'CollectionID': self.CollectionID,
            'UserID': self.UserID,
            'ProductID': self.ProductID,
            'CollectTime': self.CollectTime,
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


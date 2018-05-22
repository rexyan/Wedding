# --*--coding:utf8--*--
from Base import *
import datetime


# 创建单表
class Comment(Base):
    __tablename__ = 'comment'  # 表名
    CommentID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer)
    ProductID = Column(Integer)
    CerateTime = Column(DateTime, default=datetime.datetime.now())
    Content = Column(String(5000))
    Status = Column(Boolean, default=False)

    def __repr__(self):
        return "%s-%s" % (self.CommentID, self.UserID)

    def to_json(self):
        return {
            'CommentID': self.CommentID,
            'UserID': self.UserID,
            'ProductID': self.ProductID,
            'CerateTime': self.CerateTime,
            'Content': self.Content
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


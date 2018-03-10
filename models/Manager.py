# --*--coding:utf8--*--
from Base import *
import datetime


# 创建单表
class Manager(Base):
    __tablename__ = 'manager'  # 表名
    ManagerID = Column(Integer, primary_key=True, autoincrement=True)
    ManagerName = Column(String(100), unique=True, index=True)
    ManagerPsd = Column(String(100))
    ManagerRights = Column(String(100), nullable=True)
    ManagerTime = Column(DateTime, default=datetime.datetime.now())
    ManagerLastVisitTime = Column(DateTime, default=datetime.datetime.now())
    ManagerLastVisitIP = Column(String(100), nullable=True)

    def __repr__(self):
        return "%s-%s" % (self.ManagerID, self.ManagerName)

    def to_json(self):
        return {
            'ManagerID': self.ManagerID,
            'ManagerName': self.ManagerName,
            'ManagerPsd': self.ManagerPsd,
            'ManagerRights': self.ManagerRights,
            'ManagerTime': self.ManagerTime,
            'ManagerLastVisitTime': self.ManagerLastVisitTime,
            'ManagerLastVisitIP': self.ManagerLastVisitIP,
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


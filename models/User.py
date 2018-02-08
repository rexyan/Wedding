#--*--coding:utf8--*--
from Base import *

# 创建单表
class Users(Base):
    __tablename__ = 'users'   #表名
    UserID = Column(Integer, primary_key=True) # primary_key, 主键。必须要有主键，且主键是自增的， Integer int类型
    UserName = Column(String(100), unique=True)# unique 设置为True后此字段的值唯一 ，String  varchar类型
    UserPwd = Column(String(100))
    UserRealName = Column(String(100), nullable=True) # nullable 表示此列可以为空
    UserSex = Column(Integer, nullable=True)
    UserAge = Column(Integer, nullable=True)
    UserEmail = Column(String(100), unique=True)
    UserVip = Column(Integer, nullable=True)
    UserPoint = Column(Integer, nullable=True)
    UserCreatTime = Column(Time, nullable=True) # Time， time类型
    UserLastVisitTime = Column(Time, nullable=True)
    UserLastVisitIP = Column(String(100), nullable=True)
    
    def __repr__(self):      #当执行查询的时候返回数据，而不是对象
        return "%s-%s" %(self.id, self.name)


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
    

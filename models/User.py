#--*--coding:utf8--*--
from Base import *
import datetime

# 创建单表
class Users(Base):
    __tablename__ = 'users'  # 表名
    # xxx = Column()
    UserID = Column(Integer, primary_key=True, autoincrement=True) # primary_key, 主键。必须要有主键，且主键是自增的， Integer int类型
    UserName = Column(String(100), index=True) # String  varchar类型
    UserPwd = Column(String(100))
    UserRealName = Column(String(100), nullable=True) # nullable 表示此列可以为空
    UserSex = Column(Integer, nullable=True, default=1)
    UserAge = Column(Integer, nullable=True)
    UserEmail = Column(String(100), unique=True, index=True) # unique 设置为True后此字段的值唯一
    UserVip = Column(Integer, nullable=True, default=1)  # 默认值
    UserPoint = Column(Integer, nullable=True, default=0)
    UserCreatTime = Column(DateTime, nullable=True, default=datetime.datetime.now()) # Time， time类型
    UserLastVisitTime = Column(DateTime, nullable=True, default=datetime.datetime.now())
    UserLastVisitIP = Column(String(100), nullable=True)
    UserHashCode = Column(String(100), nullable=True)

    def __repr__(self):      #当执行查询的时候返回数据，而不是对象
        return "%s-%s" %(self.UserID, self.UserName)

    def to_json(self):
        return {
            'UserID': self.UserID,
            'UserName': self.UserName,
            'UserPwd': self.UserPwd,
            'UserRealName': self.UserRealName,
            'UserSex': self.UserSex,
            'UserAge': self.UserAge,
            'UserEmail': self.UserEmail,
            'UserVip': self.UserVip,
            'UserPoint': self.UserPoint,
            'UserCreatTime': self.UserCreatTime,
            'UserLastVisitTime': self.UserLastVisitTime,
            'UserLastVisitIP': self.UserLastVisitIP,
            'UserHashCode': self.UserHashCode,
        }

# 创建表
def init_db():
    Base.metadata.create_all(engine)

# 删除表
def drop_db():
    Base.metadata.drop_all(engine)


def main(arg):
    if arg == 1:
        init_db()
    elif arg == 0:
        drop_db()

# 如果执行的文件是当前的文件
if __name__ == '__main__':
    # 获取操控数据库的会话
    Session = sessionmaker(bind=engine)
    session = Session()
    # 执行main函数
    main(1)
    

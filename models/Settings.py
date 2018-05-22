# --*--coding:utf8--*--
from Base import *
import datetime


# 创建单表
class Setting(Base):
    __tablename__ = 'setting'  # 表名
    SettingID = Column(Integer, primary_key=True, autoincrement=True)
    WebStatus = Column(Boolean, default=True)  # 网站开关
    Logo = Column(String(100))  # 网站logo
    WebKeywords = Column(String(100))  # 网站关键字
    Webdescription = Column(String(100))  # 网站描述
    LoginBanner = Column(String(100))  # 注册页Banner

    def __repr__(self):
        return "%s-%s" % (self.SettingID)

    def to_json(self):
        return {
            'SettingID': self.SettingID,
            'WebStatus': self.WebStatus,
            'Logo': self.Logo,
            'WebKeywords': self.WebKeywords,
            'Webdescription': self.Webdescription,
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


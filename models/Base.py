# --*-- coding:utf-8--*--

# 连接数据库 sqlalchemy orm（对象关系映射）
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, MetaData
import sqlite3

# mysql:3306
# test1:数据库名称
# 设置编码: charset=utf8
# engine = create_engine("mysql://root:root@127.0.0.1:3306/test1?charset=utf8", max_overflow=5) #创建引擎，还可以加上echo=True，加上后会显示创建sql的命令
# connect_args={'check_same_thread':False}
engine = create_engine("sqlite:///data.db",connect_args={'check_same_thread':False}) #创建引擎，还可以加上echo=True，加上后会显示创建sql的命令
# engine = create_engine("postgresql://root@localhost:5432/test1") #创建引擎，还可以加上echo=True，加上后会显示创建sql的命令

# engine = create_engine('sqlite:///data.db', echo=True)
# engine = MetaData(engine)

Base = declarative_base() #创建基类

Session = sessionmaker(bind=engine)
session = Session() # 会话

NoAutoFlushSession = sessionmaker(bind=engine, autoflush=False)
noautoflushsession = NoAutoFlushSession() # 会话
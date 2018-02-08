# --*-- coding:utf-8--*--

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

engine = create_engine("mysql://root:root@127.0.0.1:3306/test1?charset=utf8", max_overflow=5) #创建引擎，还可以加上echo=True，加上后会显示创建sql的命令

Base = declarative_base() #创建基类
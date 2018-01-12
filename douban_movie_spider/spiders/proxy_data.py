# -*- coding: utf-8 -*-
# @author  ljk 
# @since   python3.6
# @history 2018/1/11
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Date,String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

try:
    engine = create_engine("mysql+pymysql://root:B0stech!@#@192.168.1.196:3306/python", max_overflow=5)
    session=sessionmaker(engine)()
except Exception:
    print(Exception,"数据库连接异常")

Base = declarative_base()
class Proxy(Base):
    __tablename__="proxy"
    id=Column(String,primary_key=True)
    ip = Column(String)  # 豆瓣详情页地址
    port = Column(String)  # 电影名称
    type = Column(String)  # 电影年份
    create_time = Column(Date)  # 影片基本信息

class Proxy_Service():
    def get_proxy_list(self):
        return session.query(Proxy).all()

    def delete(self,proxy):
        session.delete(proxy)
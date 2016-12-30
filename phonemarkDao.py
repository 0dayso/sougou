# -*- coding:utf-8 -*-
"""
File Name : 'phonemark'.py 
Description:
Author: 'wanglongzhen' 
Date: '2016/12/21' '9:36'
"""

from sqlalchemy import Column, String, create_engine, DateTime
from sqlalchemy import INT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
class phonemark(Base):
    __tablename__ = 'phonemark_new'

    phone = Column(String(15), primary_key=True)
    location = Column(String(32))
    cardtype = Column(String(64))
    tagcontent = Column(String(512))
    tagcount = Column(INT)
    ctime = Column(INT)
    source = Column(String(50))

    def __init__(self, phone, location, cardtype, tagcontent, tagcount, ctime, source):
        self.phone = phone
        self.location = location
        self.cardtype = cardtype
        self.tagcontent = tagcontent
        self.tagcount = tagcount
        self.ctime = ctime
        self.source = source


class PHONEMARK_TEST_2016_10_31(Base):
    __tablename__ = 'PHONEMARK_TEST_2016_10_31'

    phone = Column(String(15), primary_key=True)
    location = Column(String(32))
    cardtype = Column(String(64))
    tagcontent = Column(String(512))
    tagcount = Column(INT)
    ctime = Column(INT)
    source = Column(String(50))

    def __init__(self, phone, location, cardtype, tagcontent, tagcount, ctime, source):
        self.phone = phone
        self.location = location
        self.cardtype = cardtype
        self.tagcontent = tagcontent
        self.tagcount = tagcount
        self.ctime = ctime
        self.source = source

class PHONEMARK_TEST_2016_08_23(Base):
    __tablename__ = 'PHONEMARK_TEST_2016_08_23'

    phone = Column(String(15), primary_key=True)
    location = Column(String(32))
    cardtype = Column(String(64))
    tagcontent = Column(String(512))
    tagcount = Column(INT)
    ctime = Column(INT)
    source = Column(String(50))

    def __init__(self, phone, location, cardtype, tagcontent, tagcount, ctime, source):
        self.phone = phone
        self.location = location
        self.cardtype = cardtype
        self.tagcontent = tagcontent
        self.tagcount = tagcount
        self.ctime = ctime
        self.source = source

class PHONEMARK_TEST_2016_08_15(Base):
    __tablename__ = 'PHONEMARK_TEST_2016_08_15'

    phone = Column(String(15), primary_key=True)
    location = Column(String(32))
    cardtype = Column(String(64))
    tagcontent = Column(String(512))
    tagcount = Column(INT)
    ctime = Column(INT)
    source = Column(String(50))

    def __init__(self, phone, location, cardtype, tagcontent, tagcount, ctime, source):
        self.phone = phone
        self.location = location
        self.cardtype = cardtype
        self.tagcontent = tagcontent
        self.tagcount = tagcount
        self.ctime = ctime
        self.source = source

class PHONEMARK_TEST_2016_06_12(Base):
    __tablename__ = 'PHONEMARK_TEST_2016_06_12'

    phone = Column(String(15), primary_key=True)
    location = Column(String(32))
    cardtype = Column(String(64))
    tagcontent = Column(String(512))
    tagcount = Column(INT)
    ctime = Column(INT)
    source = Column(String(50))

    def __init__(self, phone, location, cardtype, tagcontent, tagcount, ctime, source):
        self.phone = phone
        self.location = location
        self.cardtype = cardtype
        self.tagcontent = tagcontent
        self.tagcount = tagcount
        self.ctime = ctime
        self.source = source

class PHONEMARK_TEST_2016_05_30(Base):
    __tablename__ = 'PHONEMARK_TEST_2016_05_30'

    phone = Column(String(15), primary_key=True)
    location = Column(String(32))
    cardtype = Column(String(64))
    tagcontent = Column(String(512))
    tagcount = Column(INT)
    ctime = Column(INT)
    source = Column(String(50))

    def __init__(self, phone, location, cardtype, tagcontent, tagcount, ctime, source):
        self.phone = phone
        self.location = location
        self.cardtype = cardtype
        self.tagcontent = tagcontent
        self.tagcount = tagcount
        self.ctime = ctime
        self.source = source

class PHONEMARK_TEST_2016_05_18(Base):
    __tablename__ = 'PHONEMARK_TEST_2016_05_18'

    phone = Column(String(15), primary_key=True)
    location = Column(String(32))
    cardtype = Column(String(64))
    tagcontent = Column(String(512))
    tagcount = Column(INT)
    ctime = Column(INT)
    source = Column(String(50))

    def __init__(self, phone, location, cardtype, tagcontent, tagcount, ctime, source):
        self.phone = phone
        self.location = location
        self.cardtype = cardtype
        self.tagcontent = tagcontent
        self.tagcount = tagcount
        self.ctime = ctime
        self.source = source


class Dao(object):

    def __init__(self):
        # 创建对象的基类:


        # 初始化数据库连接:
        engine = create_engine('mssql+pymssql://sa:mime@123@99.48.58.245/tagphone?charset=utf8', echo = True, pool_size = 20, max_overflow = 100)
        self.conn = engine.connect()

        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)

        self.session = DBSession()

        # query = self.session.query(phonemark)
        # print query.first()

    def add(self, phonemark):
        self.session.add(phonemark)
        self.session.commit()


    def query_all(self, fields, table_name = ''):
        if table_name != '':
            str_fields = ', '.join(fields)
            # ret = self.session.query(str_fields + ' from ' + table_name).all()
            ret = self.conn.execute('select ' + str_fields + ' from ' + table_name)
            for item in ret:
                for field in fields:
                    yield item[field]
        else:
            pass



    def benchInsert(self, data):
        """
        批量存数据
        :param data:
        :return:
        """
        for item in data:
            print item



if __name__ == '__main__':
    dao = Dao()


#
# class phonemark(Base):
#     __tablename__ = 'phonemark_58'
#
#     id = Column(INT, primary_key=True, autoincrement=True)
#     phone = Column(String(15))
#     location = Column(String(32))
#     cardtype = Column(String(64))
#     tagcontent = Column(String(512))
#     tagcount = Column(INT)
#     city = Column(String(50))
#     cls = Column(String(50))
#     tag1 = Column(String(50))
#     tag2 = Column(String(50))
#     tag3 = Column(String(50))
#     tag4 = Column(String(50))
#     publish_time = Column(String(50))
#     contact = Column(String(50))
#     address = Column(String(256))
#     ctime = Column(INT)
#     url = Column(String(50))
#     create_time = Column(DateTime)
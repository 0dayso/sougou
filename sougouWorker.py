# -*- coding:utf-8 -*-
"""
File Name : 'sougouSpider'.py 
Description:
Author: 'wanglongzhen' 
Date: '2016/12/20' '17:47'
"""



import requests
import ConfigParser

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, create_engine, INT, TEXT, DateTime, Integer, BIGINT
from sqlalchemy.orm import sessionmaker
import os
import codecs
import ConfigParser
from sqlalchemy.dialects.mssql import TINYINT

import sys


import message_queue
import phonemarkDao
import logging
import json
import traceback
import os
import sougouSpider
import comm_log

reload(sys)
sys.setdefaultencoding('utf8')

class sougouWorker(object):

    def __init__(self, conf_path = 'db.conf'):
        """初始化"""

        conf = ConfigParser.ConfigParser()
        conf.read(conf_path)
        mq_name = conf.get('mq', 'queue_name')

        #数据库初始化
        self.dao = phonemarkDao.Dao()

        #消息队列
        self.mq = message_queue.message(mq_name, handle_data = self.recv)

        # Log
        # logging.basicConfig(filename="output/sogou_mobile.log",
        #                     level=logging.INFO,
        #                     filemode='a',
        #                     format='%(asctime)s - %(levelname)s: %(message)s')
        # self.log = logging.getLogger("requests")
        # self.log.setLevel(logging.WARNING)
        log_name = 'worker' + str(os.getpid())
        self.log = comm_log.comm_log(log_name)

        # 初始化爬取对象

        self.spider = sougouSpider.sougouSpider()

    def send(self):
        """
        发送号码数据到消息队列
        :return:
        """
        # self.dao = phonemarkDao.Dao()

        self.log.info(u'开始发送数据到消息队列')

        table_list = ['PHONEMARK_ALL_2016_10_31', 'PHONEMARK_ALL_2016_08_23', 'PHONEMARK_ALL_2016_08_15',
                      'PHONEMARK_ALL_2016_06_12', 'PHONEMARK_ALL_2016_05_30', 'PHONEMARK_ALL_2016_05_18']
        # table_list = ['PHONEMARK_ALL_2016_10_31']


        for table_name in table_list:
            ret = self.dao.query_all(['phone'], table_name)

            for item in ret:
                # print item
                data = {'phone': item, 'table' : table_name}
                # data = {'phone': item, 'table': 'phonemark_new'}
                msg = json.dumps(data)
                self.mq.send_message(msg)

        self.log.info(u'发送数据完成')


    def recv(self, body):
        """
        从消息队列接受消息，并开始处理数据
        :return:
        """
        self.log.info(u'接受消息队列数据')
        self.log.info(body)

        try:
            # body = '{"phone": "13437116866", "table": "PHONEMARK_ALL_2016_10_31"}'
            data = json.loads(body)
            # phone = decode['phone']
            # table = decode['table']
            ret = self.do(data)

            if ret == True:
                return 1
            elif ret == False:
                return 0
        except:
            self.log.info(body)
            self.log.info(traceback.format_exc())

        return 0


    def do(self, data):
        """
        根据传输的数据进行分类
        :param phone:
        :return:
        """

        self.log.info(u'处理数据')
        self.log.info(u'数据，{0}'.format(data))

        if self.spider.being(data) == True:
            self.log.info(u'处理完成，{0}'.format(data))
            return True
        else:
            self.log.info(u'数据处理失败，{0}'.format(data))
            return False


    def begin_recv(self):
        """
        开始接受消息
        :return:
        """
        self.log.info(u'开始接收消息队列数据')
        self.mq.receive_message()



if __name__ == '__main__':

    # spider = sougouWorker()
    # spider.send()
    # spider.begin_recv()

    if len(sys.argv) == 1:
        print 'Failed'
    elif len(sys.argv) == 2:
        spider = sougouWorker()
        if sys.argv[1] == 'send':
            spider.send()
            #发送消息
            pass
        elif sys.argv[1] == 'receive':
            spider.begin_recv()
            #接受消息
        else:
            print 'param must be send or receive '
        print sys.argv[0]
        print sys.argv[1]
    else:
        print 'Failed'

    #
    # spider = sougouWorker()
    #
    # #发送
    # # spider.send()
    #
    # #接受数据并处理
    # spider.begin_recv()



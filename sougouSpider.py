# -*- coding:utf-8 -*-
"""
File Name : 'sougouSpider'.py 
Description:
Author: 'wanglongzhen' 
Date: '2016/12/26' '10:00'
"""

import time
import logging
import datetime
import sys
from bs4 import BeautifulSoup as bs
import traceback
import distinct
import pymssql
import random
import AES_Encrypt
import get_params
import json
import requests
import phonemarkDao
import proxy

reload(sys)
sys.setdefaultencoding('utf8')


class sougouSpider(object):
    def __init__(self):
        """
        初始化
        """
        #日志
        logging.basicConfig(filename="output/sougou_spider.log",
                            level=logging.INFO,
                            filemode='a',
                            format='%(asctime)s - %(levelname)s: %(message)s')
        self.log = logging.getLogger("requests")
        self.log.setLevel(logging.WARNING)

        #redis
        self.redis_name = 'phonemark_test'
        self.pool, self.redis = distinct.redis_init()

        # SQL
        self.dbhost = "99.48.58.245"
        self.dbname = "tagphone"
        self.dbusername = "sa"
        self.dbpasswd = "mime@123"

        try:
            self.conn = pymssql.connect(host=self.dbhost,
                                        database=self.dbname,
                                        user=self.dbusername,
                                        password=self.dbpasswd,
                                        charset="utf8")
        except Exception as e:
            self.conn = None
            self.log.error(u"连接数据库发生错误：" + str(e))
        else:
            self.log.info(u"成功连接到数据库!")


        self.header = {
            "Host": "data.haoma.sogou.com",
            "User-Agent": "Apache-HttpClient/UNAVAILABLE (java 1.4)",
            "Proxy-Switch-Ip" : "yes"
        }

        self.url = "http://data.haoma.sogou.com/query/super_search.php?v=1.2&parames={parames}"  # 需要计算parames
        self.hidlist = get_params.get_hidlist()

        self.aesfunc = AES_Encrypt.AES_Encrypt('Sogou$Haoma$Tong')

        # self.ses = requests.session()

        # self.proxy = proxy.Proxy()
        # self.proxy.initProxy()

    def being(self, phone):
        self.log.info(u'开始处理数据, {0}'.format(phone))
        try:
            result = distinct.check_repeate(self.redis, phone, self.redis_name)
            if result == 1:
                pass
            else:
                return False

            self.get_info_from_sogou(phone)
        except Exception, e:
            self.log.error(u'处理数据异常, 号码：{0}'.format(phone))
            self.log.error(traceback.format_exc())
            return False

        self.log.info(u'处理数据完成, {0}'.format(phone))
        return True

    def get_info_from_sogou(self, phone):
        """
        任务爬取主要部分
        :param phone:
        :return:
        """
        try:
            n = random.randint(0, 300 - 1)
            m = random.choice([2 * n - 1, 2 * n])
            paramstr = self.hidlist[m]
            if paramstr is None:
                paramstr = random.choice(self.hidlist)

            data_enc = paramstr.format(phone=phone)
            parames = self.aesfunc.encrypt(data_enc)
            url = self.url.format(parames=parames)
            ret = self.requesetGet(url)


            if ret.status_code == 403:
                self.log.info(u'代理无法使用')

            ret_json = json.loads(self.aesfunc.decrypt(ret.text))

            result_json = ret_json.get("num_info")
            if result_json is None:
                self.un_phones.append(phone)
                self.log.error(u"此号码返回None：" + str(phone))
                return
            location, cardtype, tagcontent, tagcount = result_json.get('place'), result_json.get(
                'tel_co'), result_json.get('tag'), result_json.get('amount')

            if tagcontent == '':
                source = ''
            else:
                source = 'sogou'

            try:
                phonemark = phonemarkDao.phonemark()
                phonemark.phone = phone
                phonemark.location = location
                phonemark.cardtype = cardtype
                phonemark.tagcontent = tagcontent
                phonemark.tagcount = tagcount
                phonemark.source = source
                phonemark.ctime = time.time()

                if hasattr(self, 'dao') == False:
                    self.dao = phonemarkDao.Dao()
                self.dao.add(phonemark)
            except Exception, e:
                return False

        except Exception, e:
            self.log.error(traceback.format_exc())
            return False

        return True

    def requesetGet(self, url):
        """
        统一管理request的get请求
        :param url:
        :return:
        """

        if hasattr(self, 'ses') == False:
            self.ses = requests.session()

        ret = None
        # time.sleep(2)
        begin = time.time()

        for i in range(5):
            try:
                if hasattr(self, 'proxy') == False:
                    self.proxy = proxy.proxy()

                r = self.ses.get(url, proxies = self.proxy.getProxy())

                ret = bs(r.text.encode(r.encoding), 'html.parser')
                # self.log.info(proxies)
                self.log.info(url)
            except:
                self.log.info(traceback.format_exc())
                # self.proxy.removeProxy(proxy)
            if ret != None and ret.find('404 Not Found') < 0 and ret.find('403 Forbidden') < 0:
                break

        end = time.time()
        if int(end - begin) > 100:
            # self.proxy.removeProxy(proxy)
            time_out = "URL %s, proxy %s, timeout : %0.2f " % (url, proxy, (end - begin))

        return ret

    def getProxy(self):
        # 要访问的目标页面
        # targetUrl = "http://test.abuyun.com/proxy.php"
        # targetUrl = "http://proxy.abuyun.com/switch-ip"
        targetUrl = "http://proxy.abuyun.com/current-ip"

        # 代理服务器
        proxyHost = "proxy.abuyun.com"
        proxyPort = "9010"

        # 代理隧道验证信息
        proxyUser = "H7SN5J89R653UHDP"
        proxyPass = "222E4A29D99B0499"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }

        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }

        # return proxies
        # resp = requests.get(targetUrl, proxies=proxies)
        #
        # print resp.status_code
        # print resp.text
        # print 'u'
        #
        # return proxies
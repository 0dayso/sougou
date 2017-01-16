# -*- coding:utf-8 -*-
"""
File Name : 'proxy'.py 
Description:
Author: 'wanglongzhen' 
Date: '2016/7/20' '11:14'
"""

import requests
import ConfigParser

class proxy(object):
    def __init__(self, conf_path = 'db.conf'):
        conf = ConfigParser.ConfigParser()
        conf.read(conf_path)

        # 代理服务器
        self.proxyHost = conf.get('abuproxy', 'host')
        self.proxyPort = conf.get('abuproxy', 'port')
        # 代理隧道验证信息
        self.proxyUser = conf.get('abuproxy', 'user')
        self.proxyPass = conf.get('abuproxy', 'pass')

        # self.proxyHost = "proxy.abuyun.com"
        # self.proxyPort = "9010"
        #
        # # 代理隧道验证信息
        # self.proxyUser = "H7SN5J89R653UHDP"
        # self.proxyPass = "222E4A29D99B0499"

        self.targetUrl = "http://proxy.abuyun.com/current-ip"

    def getProxy(self):
        # 要访问的目标页面
        # targetUrl = "http://test.abuyun.com/proxy.php"
        # targetUrl = "http://proxy.abuyun.com/switch-ip"
        # targetUrl = "http://proxy.abuyun.com/current-ip"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": self.proxyHost,
            "port": self.proxyPort,
            "user": self.proxyUser,
            "pass": self.proxyPass,
        }

        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }

        return proxies

    def getCurIp(self):
        proxies = self.getProxy()
        try:
            resp = requests.get(self.targetUrl, proxies=proxies)
        except Exception, e:
            return '获取代理ip失败'

        return resp.text
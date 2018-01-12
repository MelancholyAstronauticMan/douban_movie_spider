# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import json
import random
import requests
from douban_movie_spider.spiders.proxy_data import Proxy_Service


HOST="movie.douban.com"
REFERER = "https://%s/"%(HOST)
user_agent_list = json.load(open("useragent.json"))
proxy_service=Proxy_Service()
proxy_list = proxy_service.get_proxy_list()
headers = {
  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'Accept-Language':"zh-CN,zh;q=0.8",
  'Connection':'keep-alive',
  'Cache-Control':'max-age=0',
  'Host':HOST,
  'User-Agent': random.choice(user_agent_list),
  'Referer': REFERER,
}



class DoubanMovieSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def process_request(self, request, spider):
        # {"ip": "112.114.97.235", "port": "8118", "type": "HTTPS", "create_time": "2017-12-28 16:36:20"}
        request.headers['User-Agent'] = random.choice(user_agent_list)
        request.headers['Referer'] = REFERER
        request.meta["proxy"] = self.get_effective_proxy()
        return None

    def get_effective_proxy(self):
        proxy_obj = random.choice(proxy_list)
        while (not self.judge_ip(proxy_obj)):
            proxy_obj = random.choice(proxy_list)
        return "%s://%s:%s" % (proxy_obj.type.lower(), proxy_obj.ip, proxy_obj.port)

    def judge_ip(self, proxy_obj):
        # 判断ip是否可用
        type = proxy_obj.type.lower()
        if (not (type == 'https' or type == 'http')):
            print("invalid ip and port")
            return False
        proxy_url = "%s://%s:%s" % (type, proxy_obj.ip, proxy_obj.port)
        try:
            proxy_dict = {
                type: proxy_url,
            }
            response = requests.get("https://movie.douban.com/robots.txt", proxies=proxy_dict, headers=headers)
        except Exception:
            print("invalid ip and port")
            proxy_service.remove(proxy_obj)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print("effective ip:%s" % (proxy_url))
                return True
            else:
                print("invalid ip and port")
                proxy_service.remove(proxy_obj)
                return False

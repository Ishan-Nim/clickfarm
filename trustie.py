# -*- coding=utf-8 -*-
import requests
import re
import xml
import logging
import random

from bs4 import BeautifulSoup
from urllib import urlencode

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s')

class trustie:

    def __init__(self):
        self.user = '16ChengZ'
        self.passwd = 'wogongtt'
        self.cookie = 'autologin_trustie=4c3588ce4fce58c045ffd5fd8cd44bfad0aca065; _trustie_session=7a0cef1f85c99b52d92bf28af7337960'
        self.token = '/+wE3waPbgx05V/h+5/qzYlVtOYqdgmwj67uvGN5Hz0='
        self.header = {
            'Referer': 'https://www.trustie.net',
            'Host': 'www.trustie.net',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
            'Cookie': self.cookie,
        }
        self.header_post = {
            'Referer': 'https://www.trustie.net',
            'Host': 'www.trustie.net',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript,'
                      ' application/x-ecmascript',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRF-Token': self.token,
            'Cookie': self.cookie,
        }
        self.header_login = {
            'Referer': 'https://www.trustie.net/login',
            'Host': 'www.trustie.net',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept': '*text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.session = requests.Session()
        self.replies = [u'厉害了！', u'学习了。', u'看起来很不错的样子。',
                        u'深受教育。', u'赞！', u'手动点赞。',  u'非常有意义。'
                        u'支持，紫薯紫薯', u'收到']

    def login(self):
        '''
        login to site.
        :return:
        '''
        url = 'https://www.trustie.net/login'
        back_url = 'https://www.trustie.net/users/chengzhen16'
        r = self.session.get(url, headers=self.header)
        logging.info(r.cookies)
        # <meta content="oqbe7bKVQQTqMpu4KA6WC9wBfLCCYaC9RBgscy597cM=" name="csrf-token" />
        self.token = re.findall(r'<meta content="(.*?)" name="csrf-token" />', r.text)[0]
        data = [
            ('utf8', '✓'),
            ('authenticity_token', self.token),
            ('back_url', back_url),
            ('username', self.user),
            ('password', self.passwd),
            ('autologin', 1),
        ]
        serial = urlencode(data)
        logging.info(serial)
        r_post = self.session.post(url, data=serial, headers=self.header_login)
        #logging.info(r_post.text)
        logging.info(r_post.status_code)
        logging.info(r_post.cookies)
        #r = self.session.get(back_url, headers=self.header)
        #logging.info(r.text)

    def get_topics(self, url):
        '''
        get topics on url page
        :param url: specific page
        :return: dict, user_activity_id and topic post url
        '''
        r = self.session.get(url, headers=self.header)
        soup = BeautifulSoup(r.content, 'lxml')
        #soup = BeautifulSoup(open("test.html"), 'lxml')
        topics = []
        for item in soup.select(".resources"):
            temp = {}
            temp['user_activity_id'] = item['id'].strip('user_activity_')
            temp['url'] = item.select(".postGrey")[0]['href']
            topics.append(temp)
        return topics

    def reply(self, topic):
        logging.info(topic)
        url = 'https://www.trustie.net' + topic['url'] + '/replies'
        data = [
            ('utf8', '✓'),
            ('authenticity_token', self.token),
            ('quote[quote]', ''),
            ('user_activity_id', topic['user_activity_id']),
            ('reply[content]', unicode(random.choice(self.replies)).encode('utf-8')),
        ]
        serial = urlencode(data)
        logging.info('url %s', url)
        logging.info('payload %s', serial)
        r = self.session.post(url, data=serial, headers=self.header_post)
        logging.info('status: %s', r.status_code)
        if r.status_code == 200:
            return 1
        else:
            return 0


if __name__ == '__main__':
    obj = trustie()
    target = 81
    sum = 0
    i = 1
    while sum < target:
        topic_url = "https://www.trustie.net/courses/780" + "?page=" + str(i)
        topics = obj.get_topics(topic_url)
        for topic in topics:
            sum = sum + obj.reply(topic)
        i = i + 1
        logging.info("sum is %d", sum)

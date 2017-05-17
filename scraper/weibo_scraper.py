# -*- coding: utf-8 -*-
# file: sentence_similarity.py
# author: JinTian
# time: 24/03/2017 6:46 PM
# Copyright 2017 JinTian. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------
"""
using guide:
setting accounts first:

under: weibo_terminator/settings/accounts.py
you can set more than one accounts, WT will using all accounts one by one,
if one banned, another will move on.

if you care about security, using subsidiary accounts instead.

"""
import re
import sys
import os
import requests
from lxml import etree
import traceback
from pprint import pprint
from settings.config import COOKIES_SAVE_PATH
import pickle
import time
from utils.string import is_number


class WeiBoScraper(object):

    def __init__(self, using_account, uuid, filter_flag=0):
        """
        uuid user id, filter flag indicates weibo type
        :param uuid:
        :param filter_flag:
        """
        self.using_account = using_account
        self._init_cookies()
        self._init_headers()

        self.user_id = uuid
        self.filter = filter_flag
        self.user_name = ''
        self.weibo_num = 0
        self.weibo_scraped = 0
        self.following = 0
        self.followers = 0
        self.weibo_content = []
        self.num_zan = []
        self.num_forwarding = []
        self.num_comment = []
        self.weibo_detail_urls = []

    def _init_cookies(self):
        try:
            with open(COOKIES_SAVE_PATH, 'rb') as f:
                cookies_dict = pickle.load(f)
            cookies_string = cookies_dict[self.using_account]
            cookie = {
                "Cookie": cookies_string
            }
            print('setting cookies..')
            self.cookie = cookie
        except FileNotFoundError:
            print('have not get cookies yet.')

    def _init_headers(self):
        """
        avoid span
        :return:
        """
        headers = requests.utils.default_headers()
        user_agent = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko/20100101 Firefox/11.0'
        }
        headers.update(user_agent)
        print('headers: ', headers)
        self.headers = headers

    def crawl(self):
        # this is the most time-cost part, we have to catch errors, return to dispatch center
        try:
            self._get_html()
            self._get_user_name()
            self._get_user_info()
            self._get_weibo_info()
            self._get_weibo_detail_comment()
            print('weibo scrap done!')
            print('-' * 30)
            return True
        except Exception as e:
            print(e)
            print('current account being banned, return to dispatch center, resign for new account..')
            return False

    def _get_html(self):
        try:
            if is_number(self.user_id):
                url = 'http://weibo.cn/u/%s?filter=%s&page=1' % (self.user_id, self.filter)
                print(url)
            else:
                url = 'http://weibo.cn/%s?filter=%s&page=1' % (self.user_id, self.filter)
                print(url)
            self.html = requests.get(url, cookies=self.cookie, headers=self.headers).content
            print('success load html..')
        except Exception as e:
            print(e)

    def _get_user_name(self):
        print('-- getting user name')
        try:
            selector = etree.HTML(self.html)
            self.user_name = selector.xpath('//table//div[@class="ut"]/span[1]/text()')[0]
            print('current user name is: {}'.format(self.user_name))
        except Exception as e:
            print(e)
            print('html not properly loaded, maybe cookies out of date or account being banned. '
                  'change an account please')
            exit()

    def _get_user_info(self):
        print('-- getting user info')
        selector = etree.HTML(self.html)
        pattern = r"\d+\.?\d*"
        str_wb = selector.xpath('//span[@class="tc"]/text()')[0]
        guid = re.findall(pattern, str_wb, re.S | re.M)
        for value in guid:
            num_wb = int(value)
            break
        self.weibo_num = num_wb

        str_gz = selector.xpath("//div[@class='tip2']/a/text()")[0]
        guid = re.findall(pattern, str_gz, re.M)
        self.following = int(guid[0])

        str_fs = selector.xpath("//div[@class='tip2']/a/text()")[1]
        guid = re.findall(pattern, str_fs, re.M)
        self.followers = int(guid[0])
        print('current user all weibo num {}, following {}, followers {}'.format(self.weibo_num, self.following,
                                                                                 self.followers))

    def _get_weibo_info(self):
        print('-- getting weibo info')
        selector = etree.HTML(self.html)
        try:
            if selector.xpath('//input[@name="mp"]') is None:
                page_num = 1
            else:
                page_num = int(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
            pattern = r"\d+\.?\d*"
            print('--- all weibo page {}'.format(page_num))

            try:
                # traverse all weibo, and we will got weibo detail urls
                # TODO: inside for loop must set sleep avoid banned by official.
                for page in range(1, page_num):
                    url2 = 'http://weibo.cn/%s?filter=%s&page=%s' % (self.user_id, self.filter, page)
                    html2 = requests.get(url2, cookies=self.cookie, headers=self.headers).content
                    selector2 = etree.HTML(html2)
                    info = selector2.xpath("//div[@class='c']")
                    print('---- current solving page {}'.format(page))

                    if page % 10 == 0:
                        print('[ATTEMPTING] rest for 5 minutes to cheat weibo site, avoid being banned.')
                        time.sleep(60*5)

                    if len(info) > 3:
                        for i in range(0, len(info) - 2):
                            detail = info[i].xpath("@id")[0]
                            self.weibo_detail_urls.append('http://weibo.cn/comment/{}?uid={}&rl=0'.
                                                          format(detail.split('_')[-1], self.user_id))

                            self.weibo_scraped += 1
                            str_t = info[i].xpath("div/span[@class='ctt']")
                            weibos = str_t[0].xpath('string(.)')
                            self.weibo_content.append(weibos)
                            print(weibos)

                            str_zan = info[i].xpath("div/a/text()")[-4]
                            guid = re.findall(pattern, str_zan, re.M)
                            num_zan = int(guid[0])
                            self.num_zan.append(num_zan)

                            forwarding = info[i].xpath("div/a/text()")[-3]
                            guid = re.findall(pattern, forwarding, re.M)
                            num_forwarding = int(guid[0])
                            self.num_forwarding.append(num_forwarding)

                            comment = info[i].xpath("div/a/text()")[-2]
                            guid = re.findall(pattern, comment, re.M)
                            num_comment = int(guid[0])
                            self.num_comment.append(num_comment)
            except etree.XMLSyntaxError as e:
                print('get weibo info finished.')
            if self.filter == 0:
                print('共' + str(self.weibo_scraped) + '条微博')

            else:
                print('共' + str(self.weibo_num) + '条微博，其中' + str(self.weibo_scraped) + '条为原创微博')
        except IndexError as e:
            print('get weibo info done, current user {} has no weibo yet.'.format(self.user_id))

    def _get_weibo_detail_comment(self):
        """
        this is the core method, we will using self.weibo_detail_urls
        to get all weibo details and get all comments.
        :return:
        """
        weibo_comments_save_path = './weibo_detail/{}.txt'.format(self.user_id)
        if not os.path.exists(weibo_comments_save_path):
            os.makedirs(os.path.dirname(weibo_comments_save_path))
        with open(weibo_comments_save_path, 'w+') as f:
            for i, url in enumerate(self.weibo_detail_urls):
                print('solving weibo detail from {}'.format(url))
                html_detail = requests.get(url, cookies=self.cookie, headers=self.headers).content
                selector_detail = etree.HTML(html_detail)
                all_comment_pages = selector_detail.xpath('//*[@id="pagelist"]/form/div/input[1]/@value')[0]
                print('\n这是 {} 的微博：'.format(self.user_name))
                print('微博内容： {}'.format(self.weibo_content[i]))
                print('接下来是下面的评论：\n\n')

                # write weibo content
                f.writelines('E\n')
                f.writelines(self.weibo_content[i] + '\n')
                f.writelines('E\n')
                f.writelines('F\n')
                for page in range(int(all_comment_pages) - 2):

                    if page % 10 == 0:
                        print('[ATTEMPTING] rest for 5 minutes to cheat weibo site, avoid being banned.')
                        time.sleep(60*5)

                    # we crawl from page 2, cause front pages have some noise
                    detail_comment_url = url + '&page=' + str(page + 2)
                    try:
                        # from every detail comment url we will got all comment
                        html_detail_page = requests.get(detail_comment_url, cookies=self.cookie).content
                        selector_comment = etree.HTML(html_detail_page)

                        comment_div_element = selector_comment.xpath('//div[starts-with(@id, "C_")]')

                        for child in comment_div_element:
                            single_comment_user_name = child.xpath('a[1]/text()')[0]
                            if child.xpath('span[1][count(*)=0]'):
                                single_comment_content = child.xpath('span[1][count(*)=0]/text()')[0]
                            else:
                                span_element = child.xpath('span[1]')[0]
                                at_user_name = span_element.xpath('a/text()')[0]
                                at_user_name = '$' + at_user_name.split('@')[-1] + '$'
                                single_comment_content = span_element.xpath('/text()')
                                single_comment_content.insert(1, at_user_name)
                                single_comment_content = ' '.join(single_comment_content)

                            full_single_comment = '<' + single_comment_user_name + '>' + ': ' + single_comment_content
                            print(full_single_comment)
                            f.writelines(full_single_comment + '\n')
                    except etree.XMLSyntaxError as e:
                        print('-*20')
                        print('user id {} all done!'.format(self.user_id))
                        print('all weibo content and comments saved into {}'.format(weibo_comments_save_path))
                f.writelines('F\n')

    def switch_account(self, new_account):
        assert new_account.isinstance(str), 'account must be string'
        self.using_account = new_account

    def write_text(self):
        try:
            if self.filter == 1:
                result_header = '\n\n原创微博内容：\n'
            else:
                result_header = '\n\n微博内容：\n'
            result = '用户信息\n用户昵称：' + self.user_name + '\n用户id：' + str(self.user_id) + '\n微博数：' + str(
                self.weibo_num) + '\n关注数：' + str(self.following) + '\n粉丝数：' + str(self.followers) + result_header
            for i in range(1, self.weibo_scraped + 1):
                text = str(i) + ':' + self.weibo_content[i - 1] + '\n' + '点赞数：' + str(self.num_zan[i - 1]) + '	 转发数：' + str(
                    self.num_forwarding[i - 1]) + '	 评论数：' + str(self.num_comment[i - 1]) + '\n\n'
                result += text
            if not os.path.isdir('weibo'):
                os.mkdir('weibo')
            f = open("weibo/%s.txt" % self.user_id, "w")
            f.write(result)
            f.close()
            file_path = os.getcwd() + "\weibo" + "\%s" % self.user_id + ".txt"
            print('微博写入文件完毕，保存路径%s' % file_path)

        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()


def main():
    user_id = 1669879400
    filter_flag = 1
    wb = WeiBoScraper(user_id, filter_flag)
    wb.crawl()
    print('用户名：', wb.user_name)
    print('全部微博数：', str(wb.weibo_num))
    print('关注数：', str(wb.following))
    print('粉丝数：', str(wb.followers))
    print('最新一条微博为：', wb.weibo_content[0])
    print('最新一条微博获得的点赞数：', wb.num_zan[0])
    print('最新一条微博获得的转发数：', str(wb.num_forwarding[0]))
    print('最新一条微博获得的评论数：', str(wb.num_comment[0]))
    wb.write_text()


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
# file: dispatch_center.py
# author: JinTian
# time: 13/04/2017 9:52 AM
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
from scraper.weibo_scraper import WeiBoScraper
from settings.config import COOKIES_SAVE_PATH
from settings.accounts import accounts
import os
from utils.cookies import get_cookie_from_network
import pickle


class Dispatcher(object):
    """
    Dispatch center, if your cookies is out of date,
    set update_cookies to True to update all accounts cookies
    """

    def __init__(self, id_file_path, mode, uid, filter_flag=0, update_cookies=False):
        self.mode = mode
        self.filter_flag = filter_flag
        self.update_cookies = update_cookies

        self._init_accounts_cookies()
        self._init_accounts()

        if self.mode == 'single':
            self.user_id = uid
        elif self.mode == 'multi':
            self.id_file_path = id_file_path
        else:
            raise 'mode option only support single and multi'

    def execute(self):
        if self.mode == 'single':
            self._init_single_mode()
        elif self.mode == 'multi':
            self._init_multi_mode()
        else:
            raise 'mode option only support single and multi'

    def _init_accounts_cookies(self):
        """
        get all cookies for accounts, dump into pkl, this will only run once, if
        you update accounts, set update to True
        :return:
        """
        if self.update_cookies:
            for k, v in accounts:
                get_cookie_from_network(k, v)
            print('all accounts updated cookies finished. starting scrap..')
        else:
            if os.path.exists(COOKIES_SAVE_PATH):
                pass
            else:
                for k, v in accounts:
                    get_cookie_from_network(k, v)
                print('all accounts getting cookies finished. starting scrap..')

    def _init_accounts(self):
        """
        setting accounts
        :return:
        """
        try:
            with open(COOKIES_SAVE_PATH, 'rb') as f:
                cookies_dict = pickle.load(f)
            self.all_accounts = list(cookies_dict.keys())
            print('----------- detected {} accounts, weibo_terminator will using all accounts to scrap '
                  'automatically -------------'.format(len(self.all_accounts)))
            print('detected accounts: ', self.all_accounts)
        except Exception as e:
            print(e)
            print('error, not find cookies file.')
      
    def _init_single_mode(self):
        scraper = WeiBoScraper(using_account=self.all_accounts[0], uuid=self.user_id, filter_flag=self.filter_flag)
        i = 1
        while True:
            result = scraper.crawl()
            if result:
                print('finished!!!')
                break
            else:
                if i >= len(self.all_accounts):
                    print('scrap not finish, account resource run out. update account move on scrap.')
                    break
                else:
                    scraper.switch_account(self.all_accounts[i])
                    print('account {} being banned or error weibo is none for current user id, switch to {}..'.format(
                        self.all_accounts[i - 1], self.all_accounts[i]))

    def _init_multi_mode(self):
        pass



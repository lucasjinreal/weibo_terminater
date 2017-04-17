# -*- coding: utf-8 -*-
# file: tests.py
# author: JinTian
# time: 17/04/2017 2:40 PM
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
from utils.cookies import get_cookie_from_network
from settings.accounts import accounts
from settings.config import COOKIES_SAVE_PATH, DEFAULT_USER_ID
import pickle
import requests


def test():
    cookies = get_cookie_from_network(accounts[0]['id'], accounts[0]['password'])
    print(cookies)


def test_for_cookies():
    with open(COOKIES_SAVE_PATH, 'rb') as f:
        cookies_dict = pickle.load(f)
    print(cookies_dict)
    user_id = '15116123160'
    url = 'http://weibo.cn/u/%s?filter=%s&page=1' % (DEFAULT_USER_ID, 0)
    print(url)

    cookie = {
        "Cookie": cookies_dict[user_id]
    }
    print(list(cookies_dict.keys()))

def test_numric():
    a = '124556'
    b = './huogeh/grjtioh'
    print(float(a))
    print(float(b))

if __name__ == '__main__':
    test_numric()
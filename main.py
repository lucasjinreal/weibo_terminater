# -*- coding: utf-8 -*-
# file: main.py
# author: JinTian
# time: 13/04/2017 10:01 AM
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
import argparse

from core.dispatch_center import Dispatcher
from settings.config import DEFAULT_USER_ID
from utils.string import is_valid_id


def parse_args():
    parser = argparse.ArgumentParser(description='WeiBo Terminator. Jin Fagang')

    help_ = 'set user id. or if_file contains multi ids.'
    parser.add_argument('-i', '--id', default=DEFAULT_USER_ID, help=help_)

    help_ = 'set weibo filter flag. if filter is 0, then weibo are all original,' \
            ' if 1, weibo contains repost one. default is 0.'
    parser.add_argument('-f', '--filter', default='1', help=help_)

    help_ = 'debug mode for develop. set 1 on, set 0 off.'
    parser.add_argument('-d', '--debug', default='1', help=help_)

    args_ = parser.parse_args()
    return args_


if __name__ == '__main__':
    args = parse_args()
    if args.debug == '1':
        uid = args.id
        if not '/' or '\\' in uid:
            print('debug mode not support id file.')
        else:
            if not args.filter:
                filter_flag = args.filter
            else:
                filter_flag = 0
            print('[debug mode] crawling weibo from id {}'.format(uid))
            dispatcher = Dispatcher(id_file_path=None, mode='single', uid=uid, filter_flag=filter_flag)
            dispatcher.execute()
    elif args.debug == '0':
        uid = args.id
        if not '/' or '\\' in uid:
            if not args.filter:
                filter_flag = args.filter
            else:
                filter_flag = 0
            print('crawling weibo from id {}'.format(uid))
            dispatcher = Dispatcher(id_file_path=None, mode='single', uid=uid, filter_flag=filter_flag)
            dispatcher.execute()
        else:
            if not args.filter:
                filter_flag = args.filter
            else:
                filter_flag = 0
            print('crawling weibo from multi id file {}'.format(uid))
            dispatcher = Dispatcher(id_file_path=uid, mode='multi', uid=None, filter_flag=filter_flag)
            dispatcher.execute()
    else:
        print('debug mode error, set 1 on, set 0 off.')

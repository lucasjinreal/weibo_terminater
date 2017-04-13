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


class Dispatcher(object):

    def __init__(self, id_file_path, mode, uid, filter_flag=0):
        self.mode = mode
        self.filter_flag = filter_flag

        if self.mode == 'single':
            self.user_id = uid
            self._init_single_mode()
        elif self.mode == 'multi':
            self.id_file_path = id_file_path
            self._init_multi_mode()
        else:
            raise 'mode option only support single and multi'
      
    def _init_single_mode(self):
        self.execute(self.user_id, self.filter_flag)

    def _init_multi_mode(self):
        pass

    @staticmethod
    def execute(user_id, filter_flag):
        scraper = WeiBoScraper(uuid=user_id, filter_flag=filter_flag)
        scraper.crawl()

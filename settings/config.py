# -*- coding: utf-8 -*-
# file: settings.py
# author: JinTian
# time: 13/04/2017 10:10 AM
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
all configurations set here, follow the instructions
"""

# you should not change this properly
DEFAULT_USER_ID = 'realangelababy'
LOGIN_URL = 'https://passport.weibo.cn/signin/login'

ID_FILE_PATH = './settings/id_file'


# change this to your PhantomJS unzip path, point to bin/phantomjs executable file, full path
PHANTOM_JS_PATH = '/home/jintian/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'


COOKIES_SAVE_PATH = 'settings/cookies.pkl'

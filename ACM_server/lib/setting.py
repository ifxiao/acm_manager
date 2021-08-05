#!/user/bin/env python3
# _*_ coding: utf-8 _*_

from __future__ import unicode_literals
from __future__ import division
import sys
import os

MAIN_DIR_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))

ACM_MANAGER_CONF = {'DB_HOST': '159.75.101.220',
                          'DB_PORT': 3306,
                          'DB_USER_NAME': 'root',
                          'DB_PASSWORD': 'root@2017',
                          'DB_DATABASE_NAME': 'karl'
                          }

ACM_MANAGER_CONF_back = {
                        'DB_HOST': '127.0.0.1',
                          'DB_PORT': 3306,
                          'DB_USER_NAME': 'root',
                          'DB_PASSWORD': 'kh123456',
                          'DB_DATABASE_NAME': 'karl'
}

HUSTOJ_ONLINE_CONF = {'DB_HOST': '127.0.0.1',
                      'DB_PORT': 3306,
                      'DB_USER_NAME': 'root',
                      'DB_PASSWORD': 'root@csti',
                      'DB_DATABASE_NAME': 'jol'
                    }

CONTEST_CONF = {'DB_HOST': '',
                  'DB_PORT': 3306,
                  'DB_USER_NAME': 'root',
                  'DB_PASSWORD': 'root@csti',
                  'DB_DATABASE_NAME': 'jol'
                }

SSH_TUNNEL_CONF = {'HOST':  '123.206.8.101',
                   'PORT': 22,
                   'USER_NAME': 'root',
                   'PASSWORD': 'root@csti'
                   }

HUSTOJ_CONTEST_CONF = {'DB_HOST': '127.0.0.1',
                      'DB_PORT': 3306,
                      'DB_USER_NAME': 'acm_admin',
                      'DB_PASSWORD': 'acm117',
                      'DB_DATABASE_NAME': 'jol'
                    }

SSH_CONNTEST_CONF = {'HOST':  '192.168.1.253',
                   'PORT': 22,
                   'USER_NAME': 'acm117',
                   'PASSWORD': '86609674'
                   }






IS_HK = False

# 0为体验网（不使用代理）， 1为办公网络， 2为开发网络，3为部署机器（使用L5的IP池）
NET_TYPE = 2
COROUTINE_NUM = 50

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division
import six

import re
import sys
import os
import json
import time
from six.moves import cPickle as pickle
import logging
import logging.handlers
import setting
import pymysql
import platform
import tempfile
import hashlib

LOG_FILE_PATH = os.path.join(setting.MAIN_DIR_PATH, "log.txt")

G_global_dict = {}



def get_now_str():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d-%H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp

def get_variable_names(obj):
    import inspect
    frame = inspect.currentframe()
    try:
        names = [name for name, val in frame.f_back.f_locals.items() if val is obj]
        names += [name for name, val in frame.f_back.f_globals.items()
                  if val is obj and name not in names]
        return names
    finally:
        del frame

def getTempFilePath():
    defult_tmp_dir = tempfile._get_default_tempdir()
    temp_name = next(tempfile._get_candidate_names())
    return os.path.join(defult_tmp_dir, temp_name)

def cleanTrackName(track_name):
    track_name = track_name.lower().strip()
    track_name = re.sub(r'＜[^)]*＞', '', track_name).lower().strip()
    track_name = re.sub(r'<[^)]*>', '', track_name).lower().strip()
    track_name = re.sub(r'\[[^)]*\]', '', track_name).lower().strip()
    track_name = re.sub(r'\([^)]*\)', '', track_name).lower().strip()
    return re.sub(r'（[^)]*）', '', track_name).lower().strip()

def set_global_value(key, value):
    global G_global_dict
    G_global_dict[key] = value

def get_global_value(key, defValue=None):
    global G_global_dict
    try:
        return G_global_dict[key]
    except KeyError:
        return defValue

def initRotateLog(logFile=os.path.join(setting.MAIN_DIR_PATH, 'log') , logName="" , logLevel=logging.DEBUG, maxBytes=100*1024*1024 , backupCount = 5):
    if not os.path.isfile(logFile):
        confirm_path(logFile)
    handler = logging.handlers.RotatingFileHandler(logFile, maxBytes = 100*1024*1024, backupCount = 5, encoding='utf8')
    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logger = logging.getLogger(logName)
    logger.addHandler(handler)
    logger.setLevel(logLevel)
    return logger

def getGlobalLog():
    global LOG_FILE_PATH
    G_log = get_global_value("G_log")
    if not G_log:
        G_log = initRotateLog(logFile=LOG_FILE_PATH)
        set_global_value("G_log", G_log)
    return G_log

def getMainDir():
    pass

def make_dir_if_not_exit(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def confirm_path(fname):
    dirName = os.path.dirname(fname)
    if not os.path.isdir(dirName) and len(dirName)>0:
        os.makedirs(dirName)

def delete_illegal_character_of_file_name(file_name):
    illegal_character_list = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for illegal_character in illegal_character_list:
        file_name = file_name.replace(illegal_character, ' ')
    return file_name

def jsonDump(obj, file_path):
    with open(file_path, 'w', encoding='utf8') as fout:
        json.dump(obj, fout)

def jsonLoad(file_path):
    with open(file_path, 'r') as fin:
        return json.load(fin)

def pickleDump(obj, file_path):
    with open(file_path, 'wb') as fout:
        pickle.dump(obj, fout)

def pickleLoad(file_path):
    with open(file_path, 'rb') as fin:
        return pickle.load(fin)

def divide_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def divide_list_begin_from(l, n, begin_from):
    for i in range(begin_from, len(l), n):
        yield l[i:i+n]

def divide_to_n_list(ls, n):
    if not isinstance(ls,list):
        ls = list(ls)
    if n <= 0:
        return []
    elif n > len(ls):
        result_lists = [[i] for i in ls]
        result_lists.extend([[] for i in range(n - len(ls))])
        return result_lists
    elif n == len(ls):
        return [[i] for i in ls]
    else:
        j = len(ls) // n
        ls_return = []
        for i in range(0, (n-1)*j, j):
            ls_return.append(ls[i:i+j])
        ls_return.append(ls[(n-1)*j:])
        return ls_return

def myPrint(content):
    if isinstance(content, six.text_type):
        sys.stdout.buffer.write((content+'\n').encode('utf8'))
    elif isinstance(content, six.binary_type):
        sys.stdout.buffer.write(content+'\n'.encode('utf8'))
    else:
        sys.stdout.buffer.write((str(content)+'\n').encode('utf8'))
    sys.stdout.buffer.flush()

def DbEscape(db, content):
    result = db.escape(content)
    if (not result.startswith("'")) and (not result.endswith("'")):
        return "'{0}'".format(result)
    elif result.startswith("'") and result.endswith("'"):
        return result
    else:
        raise SyntaxError

def myJoin(split_str, string_list):
    return split_str.join([str(string) for string in string_list])


LOG_FILE_PATH = os.path.join(setting.MAIN_DIR_PATH, "log.txt")

G_global_dict = {}



def getConnection(db_conf, result_type=list, autocommit=True, ssh_status=False, SSH_TUNNEL_CONF = None):
    ssh_conf = None
    if ssh_status:
        if SSH_TUNNEL_CONF is not None:
            ssh_conf = SSH_TUNNEL_CONF
        else:
            ssh_conf = setting.SSH_TUNNEL_CONF
    cursorclass = pymysql.cursors.Cursor
    if result_type == dict:
        cursorclass = pymysql.cursors.DictCursor
    if ssh_conf:
        try:
            print(ssh_conf)
            from sshtunnel import SSHTunnelForwarder
            server = SSHTunnelForwarder(
                ssh_address_or_host=(ssh_conf['HOST'], ssh_conf['PORT']),  # 指定ssh登录的跳转机的address
                ssh_username=ssh_conf['USER_NAME'],  # 跳转机的用户
                ssh_password=ssh_conf['PASSWORD'],  # 跳转机的密码
                remote_bind_address=(db_conf['DB_HOST'], db_conf['DB_PORT']))
            server.start()
        except Exception as e:
            print(e)
        connection = pymysql.connect(host='127.0.0.1', user=db_conf['DB_USER_NAME'], passwd=db_conf['DB_PASSWORD'], db=db_conf['DB_DATABASE_NAME'], port=server.local_bind_port,cursorclass=cursorclass, charset='utf8mb4', autocommit=autocommit)
        my_close = connection.close
        def wrap_close():
            my_close()
            server.stop()
        connection.close = wrap_close
        return connection
    else:
        return pymysql.connect(host=db_conf['DB_HOST'], user=db_conf['DB_USER_NAME'],
                               passwd=db_conf['DB_PASSWORD'],
                               db=db_conf['DB_DATABASE_NAME'], port=db_conf['DB_PORT'],
                               cursorclass=cursorclass, charset='utf8mb4', autocommit=autocommit)

def encode_md5(from_str):
    m = hashlib.md5()
    m.update(str(from_str).encode("utf8"))
    return(m.hexdigest())

def get_conf_connect():
    return getConnection(setting.MUSIC_READONLY_DB_CONF)

def get_lyric_connect():
    return getConnection(setting.DB_LYRIC_DB)

def get_embedding_connect():
    return getConnection(setting.DB_EMBEDDING_DB)
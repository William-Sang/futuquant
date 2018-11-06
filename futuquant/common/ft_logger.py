# -*- coding: utf-8 -*-

import logging
from datetime import datetime
import os
import platform


# logger = logging.getLogger('FT')
# log_level = logging.INFO
# is_file_log = True
#
# # 设置logger的level为DEBUG
# logger.setLevel(log_level)
#
# # 创建一个输出日志到控制台的StreamHandler
# hdr = logging.StreamHandler()
# formatter = logging.Formatter(
#     '%(asctime)s [%(filename)s] %(funcName)s:%(lineno)d: %(message)s')
# hdr.setFormatter(formatter)
#
# # 给logger添加上handler
# logger.addHandler(hdr)
#
# # 添加文件handle
# if is_file_log:
#     filename = 'ft_' + datetime.now().strftime('%Y%m%d') + '.log'
#     tempPath = os.path.join(os.getcwd(), 'log')
#     if not os.path.exists(tempPath):
#         os.makedirs(tempPath)
#     filepath = os.path.join(tempPath, filename)
#     fileHandler = logging.FileHandler(filepath)
#     fileHandler.setFormatter(formatter)
#     logger.addHandler(fileHandler)
#
#
# def make_log_msg(title, **kwargs):
#     msg = ''
#     if len(kwargs) > 0:
#         msg = ':'
#         for k, v in kwargs.items():
#             msg += ' {0}={1};'.format(k, v)
#     return title + msg




__LogName__ = "com.futunn.FutuOpenD//Log"

sys_str = platform.system()
if sys_str == "Linux":
    import pwd


class FTLog(object):

    BOTH_FILE_CONSOLE = 3
    ONLY_FILE = 1
    ONLY_CONSOLE = 2

    def __init__(self, **args):
        sys_str = platform.system()
        if sys_str == "Windows":
            self.log_path = os.path.join(os.getenv("appdata"), __LogName__)
        else:
            pwd_name = pwd.getpwuid(os.getuid())[0]
            self.log_path = os.path.join(pwd_name, __LogName__)

        file_level = logging.DEBUG
        console_level = logging.ERROR

        if "file_level" in args:
            file_level = args["file_level"]
        if "console_level" in args:
            console_level = args["console_level"]

        self.file_logger = logging.getLogger('FTFileLog')
        self.file_logger.setLevel(file_level)
        self.console_logger = logging.getLogger('FTConsoleLog')
        self.console_logger.setLevel(console_level)

        self.formatter = logging.Formatter('%(asctime)s [%(filename)s] %(funcName)s:%(lineno)d: %(message)s')

        if not hasattr(self, 'fileHandler'):
            file_name = 'ft_' + datetime.now().strftime('%Y%m%d') + '.log'
            file_path = os.path.join(self.log_path, file_name)
            self.fileHandler = logging.FileHandler(file_path)
            self.fileHandler.setLevel(file_level)
            self.fileHandler.setFormatter(self.formatter)
            self.file_logger.addHandler(self.fileHandler)

        if not hasattr(self, 'consoleHandler'):
            self.consoleHandler = logging.StreamHandler()
            self.consoleHandler.setLevel(console_level)
            self.consoleHandler.setFormatter(self.formatter)
            self.console_logger.addHandler(self.consoleHandler)

    def __new__(cls):
        # 关键在于这，每一次实例化的时候，我们都只会返回这同一个instance对象
        if not hasattr(cls, 'instance'):
            cls.instance = super(FTLog, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def make_log_msg(title, **kwargs):
        msg = ''
        if len(kwargs) > 0:
            msg = ':'
            for k, v in kwargs.items():
                msg += ' {0}={1};'.format(k, v)
        return title + msg

    def warning2(self, flag, msg, *args, **kwargs):
        if (flag & self.ONLY_FILE) != 0:
            self.file_logger.warning(msg, *args, **kwargs)
        if (flag & self.ONLY_CONSOLE) != 0:
            self.console_logger.warning(msg, *args, **kwargs)

    def error2(self, flag, msg, *args, **kwargs):
        if (flag & self.ONLY_FILE) != 0:
            self.file_logger.error(msg, *args, **kwargs)
        if (flag & self.ONLY_CONSOLE) != 0:
            self.console_logger.error(msg, *args, **kwargs)

    def debug2(self, flag, msg, *args, **kwargs):
        if (flag & self.ONLY_FILE) != 0:
            self.file_logger.debug(msg, *args, **kwargs)
        if (flag & self.ONLY_CONSOLE) != 0:
            self.console_logger.debug(msg, *args, **kwargs)

    def info2(self, flag, msg, *args, **kwargs):
        if (flag & self.ONLY_FILE) != 0:
            self.file_logger.info(msg, *args, **kwargs)
        if (flag & self.ONLY_CONSOLE) != 0:
            self.console_logger.info(msg, *args, **kwargs)

    def file_warning(self, msg, *args, **kwargs):
        self.file_logger.warning(msg, *args, **kwargs)

    def file_error(self, msg, *args, **kwargs):
        self.warning(msg, *args, **kwargs)

    def file_debug(self, msg, *args, **kwargs):
        self.file_logger.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.warning2(self.BOTH_FILE_CONSOLE, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.error2(self.BOTH_FILE_CONSOLE, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.debug2(self.BOTH_FILE_CONSOLE, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.info2(self.BOTH_FILE_CONSOLE, msg, *args, **kwargs)


logger = FTLog()

if __name__ == '__main__':
    logger.error2(FTLog.BOTH_FILE_CONSOLE, "1111111111")
    logger.error2(FTLog.ONLY_FILE, "222222222")
    logger.error2(FTLog.ONLY_CONSOLE, "33333333")
    logger.debug('444444444 %s' % datetime.now())


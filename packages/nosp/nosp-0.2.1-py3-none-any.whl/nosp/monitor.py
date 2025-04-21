import atexit
import os
import sys
import threading
import time
import uuid
from datetime import datetime
from pathlib import Path
import traceback

import requests
from loguru import logger
import socket


class SpiderInfo(object):

    def __init__(self, name=None, group_name=None, monitor=False, monitor_endpoint='http://127.0.0.1:12000/endpoint'):
        self._monitor_endpoint = monitor_endpoint
        self.pid = str(os.getpid())
        self.uid = str(uuid.uuid4())
        self.name = name
        self.group_name = group_name
        self.start_time = time.time()
        self.end_time = None
        self.run_time = None
        self.log_file = None
        self.file = None
        self.interpreter = sys.executable
        # 0 初始化，1 启动，2 完成，-1 异常
        self.status = 0
        self.insert_count = 0
        self.progress = 0
        self.total_progress = 0
        self.exception = None
        self.exception_stack = None
        self.server = os.getenv("SERVER_NAME")
        # self.user = os.getenv("SERVER_USER")
        self.__is_monitor = monitor
        self.__get_script_info()
        # 设置全局异常捕获器
        sys.excepthook = self.__global_exception_handler
        # 注册函数到程序退出时调用
        atexit.register(self.__before_exit)

        if self.log_file:
            logger.add(self.log_file, rotation="50 MB")
        self.status = 1

        if self.__is_monitor:
            self.start_monitor()

        self.__lock = threading.Lock()

        self.lan_ip = '127.0.0.1'
        self.wan_ip = '0.0.0.0'
        self.__init_ip()

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    def __global_exception_handler(self, exc_type, exc_value, exc_traceback):
        # logger.error({"exception": str(exc_type), "msg": str(exc_value), })
        stack_trace = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logger.error(f"Exception occurred: {exc_type.__name__}: {exc_value}\nStack Trace:\n{stack_trace}")
        self.exception_stack = stack_trace
        self.exception = str(exc_type) + ':' + str(exc_value)
        self.status = -1
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    def __before_exit(self):
        self.end_time = time.time()
        self.run_time = self.end_time - self.start_time
        if self.status != -1:
            self.status = 2
        logger.warning(f'run_time:{self.run_time} s')
        if self.__is_monitor:
            self.notice()
        logger.warning(self)

    def __get_script_info(self):
        # 获取主模块的文件名
        main_module = sys.modules.get('__main__')
        filepath = main_module.__file__
        log_file = self.__get_log_path(filepath)
        self.file = filepath
        self.log_file = log_file

    def __get_log_path(self, file_path: str) -> str:
        base_log_path = Path("C:\\logs") if sys.platform == "win32" else Path("/logs")
        original_path = Path(file_path)
        stem_name = original_path.stem
        timestamp = datetime.now().strftime("%m%d-%H%M%S.%f")[:-3].replace('.', '')
        log_filename = f"{stem_name}-{timestamp}.log"
        if sys.platform == "win32":
            drive, rel_path = os.path.splitdrive(original_path.parent)
        else:
            rel_path = str(original_path.parent)
        rel_path = rel_path.lstrip(os.sep)
        full_path = base_log_path / rel_path / log_filename
        # full_path.parent.mkdir(parents=True, exist_ok=True)
        return str(full_path)

    def __monitor(self):
        """
        10s 上传一次数据到后台，监控程序运行
        :return:
        """
        num = 0
        while True:
            result = self.notice()
            if not result:
                num += 1
                if num == 100:
                    logger.error('上报数据失败，终止上报')
                    break
            time.sleep(10)

    def notice(self):
        try:
            requests.post(url=self._monitor_endpoint, json=self.to_dict(), timeout=4)
            return True
        except Exception as e:
            return False

    def start_monitor(self):
        mt = threading.Thread(target=self.__monitor)
        mt.setDaemon(True)
        mt.start()

    def update_count(self, v: int = 1):
        with self.__lock:
            self.insert_count += v

    def add_count(self, v: int = 1):
        with self.__lock:
            self.insert_count += v

    def __repr__(self):
        return (
            f"SpiderInfo(pid={self.pid}, uid={self.uid}, name={self.name}, group={self.group_name}, lan_ip={self.lan_ip}, wan_ip={self.wan_ip}) "
            f"start_time={self.start_time}, end_time={self.end_time}, "
            f"run_time={self.run_time}, log_file={self.log_file}, "
            f"file={self.file}, interpreter={self.interpreter}, "
            f"status={self.status}, insert_count={self.insert_count}, "
            f"progress={self.progress}, total_progress={self.total_progress}, "
            f"exception={self.exception})")

    def __init_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("223.5.5.5", 80))
            lan_ip = s.getsockname()[0]
            s.close()
            self.lan_ip = lan_ip
        except Exception as e:
            try:
                self.lan_ip = socket.gethostbyname(socket.gethostname())
            except:
                pass
        wan_ip = os.getenv("WAN_IP", '0.0.0.0')
        if wan_ip == '0.0.0.0':
            try:
                response = requests.get('https://ipinfo.io/json', timeout=5)
                wan_ip = response.json()['ip']
            except:
                pass
        self.wan_ip = wan_ip


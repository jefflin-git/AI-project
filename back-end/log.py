import logging
import sys
from common.constants import MODE

class Logger:
    def __init__(self, name: str, log_file_path: str = None):
        # 建立 logger
        self.logger = logging.getLogger(name)
        if MODE == "DEBUG":
            self.logger.setLevel(logging.DEBUG)
        elif MODE == "INFO":
            self.logger.setLevel(logging.INFO)
        elif MODE == "WARNING":
            self.logger.setLevel(logging.WARNING)
        elif MODE == "ERROR":
            self.logger.setLevel(logging.ERROR)
        self.formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s')
        self.log_file_path = log_file_path
        self.set_log_console()
        if self.log_file_path != None:
            self.set_log_file()
        
    def set_log_console(self):
        # 建立「控制台」處理器 (輸出到螢幕)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)
    
    def set_log_file(self):
        # 建立檔案處理器 (File Handler)
        file_handler = logging.FileHandler(self.log_file_path, encoding='utf-8')
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message, exc_info=True)
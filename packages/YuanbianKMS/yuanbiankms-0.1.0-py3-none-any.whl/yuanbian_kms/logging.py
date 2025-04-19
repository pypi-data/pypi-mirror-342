# -*- coding=utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler
formatter = logging.Formatter('%(asctime)s - %(process)d-%(threadName)s - '
                              '%(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')

log_file_handle = RotatingFileHandler("app.log",
                                              maxBytes=1000 * 1024,
                                              backupCount=1,
                                              encoding="utf-8"
                                              )
log_file_handle.setFormatter(formatter)

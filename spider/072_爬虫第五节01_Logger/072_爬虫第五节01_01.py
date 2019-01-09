# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 11:29:27 2017

@author: natasha1_Yang
"""

import logging
import logging.config

logging.config.fileConfig("072_logger_00.conf")

logger = logging.getLogger("simpleExample")

logger.debug("debug message")
logger.info("info message")
logger.warn("warn message")
logger.error("error message")
logger.critical("critical message")
import logging
import logging.config

logging.config.fileConfig("logging.properties")
#logger = logging.getLogger("simpleExample")
logger = logging.getLogger()

def greet(arg):
   print('Hiya ', arg)
   logger.debug("debug message")
   logger.info("info message")
   logger.warn("warn message")

def swear(arg):
   print('Bugger off ', arg)
   logger.error("error message")
   logger.critical("critical message")

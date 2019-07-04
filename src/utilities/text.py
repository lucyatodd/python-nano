import logging
import logging.config

logging.config.fileConfig("logging.properties")
logger = logging.getLogger("simpleExample")
#3logger = logging.getLogger()

def greet(arg):
   print('Hiya ', arg)
   logger.debug("debug message detail we not ready just started coding")
   logger.info("info message getting confident")
   logger.warn("warn message working and tested")

def swear(arg):
   print('Bugger off ', arg)
   logger.error("error message")
   logger.critical("critical message")

import logging
from logging.handlers import RotatingFileHandler

Rthandler = RotatingFileHandler('last.log', maxBytes=10 * 1024 * 1024, backupCount=5)
Rthandler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

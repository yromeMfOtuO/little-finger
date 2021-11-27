"""日志"""
import logging
import re
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('werkzeug')
logger.setLevel(logging.DEBUG)
# 按天切分日志
handler = TimedRotatingFileHandler(
    filename='./log.log',
    when='midnight',
    backupCount=7,
    encoding='utf-8'
)
handler.suffix = '%Y-%m-%d.log'
handler.extMatch = re.compile(r'^\d{4}-\d{2}-\d{2}.log')
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s")
)
logger.addHandler(handler)


if __name__ == '__main__':
    logger.info('test log')
    logger.info('test log2')
    logger.info('test log3')

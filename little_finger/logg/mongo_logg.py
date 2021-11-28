"""mongo 日志"""

import logging.config
# from log4mongo.handlers import MongoHandler

config = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'log.log',
            'level': 'DEBUG',
            'formatter': 'simple'
        },
        'mongo': {
            'class': 'log4mongo.handlers.MongoHandler',
            'host': 'host',
            # 'port': 27017,
            'database_name': 'mongo_logs',
            'collection': 'logs',
            'level': 'DEBUG',
            'username': 'username',
            'password': 'password'
        },
    },
    'loggers':{
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
            # 'propagate': True,
        },
        # 这里也配置了文件使用 console 和 file 的 logger
        'simple': {
            'handlers': ['console', 'file'],
            'level': 'WARN',
        },
        'mongo': {
            'handlers': [
                'console',
                # 'file',
                'mongo'
            ],
            'level': 'DEBUG',
        }
    }
}

logging.config.dictConfig(config)
mlogger = logging.getLogger('mongo')


if __name__ == '__main__':
    mlogger.debug('debug message')
    mlogger.info('info message')
    mlogger.warn('warn message')
    mlogger.error('error message')
    mlogger.critical('critical message')

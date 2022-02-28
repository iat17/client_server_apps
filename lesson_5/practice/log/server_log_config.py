import sys
import os
import logging
import logging.handlers
# sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append('../')
from common.variables import LOGGING_LEVEL


formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(filename)s %(message)s')

path_to_dir = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(path_to_dir, 'server.log')

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.ERROR)
log_file = logging.handlers.TimedRotatingFileHandler(path, encoding='utf8', interval=1, when='S')
log_file.setFormatter(formatter)

logger = logging.getLogger('server')
logger.addHandler(stream_handler)
logger.addHandler(log_file)
logger.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    logger.critical('critical error')
    logger.error('error')
    logger.debug('debug')
    logger.info('information')

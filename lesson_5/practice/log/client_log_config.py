import sys
import os
import logging
sys.path.append('../')
from common.variables import LOGGING_LEVEL

formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(filename)s %(message)s')

path_to_dir = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(path_to_dir, 'client.log')

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.ERROR)
LOG_FILE = logging.FileHandler(path, encoding='utf8')
LOG_FILE.setFormatter(formatter)

LOGGER = logging.getLogger('client')
LOGGER.addHandler(stream_handler)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    LOGGER.critical('critical error')
    LOGGER.error('error')
    LOGGER.debug('debug')
    LOGGER.info('information')

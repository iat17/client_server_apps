import os
import logging


DEFAULT_PORT = int(os.getenv('DEFAULT_PORT', 7777))
DEFAULT_IP_ADDRESS = os.getenv('DEFAULT_IP_ADDRESS', '127.0.0.1')

MAX_CONNECTIONS = int(os.getenv('MAX_CONNECTIONS', 5))

MAX_PACKAGE_LENGTH = 1024

ENCODING = 'utf-8'

ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'sender'
DESTINATION = 'to'

PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'message_text'
EXIT_MESSAGE = 'exit'

RESP_200 = {RESPONSE: 200}
RESP_400 = {
    RESPONSE: 400,
    ERROR: None
}

LOGGING_LEVEL = logging.DEBUG

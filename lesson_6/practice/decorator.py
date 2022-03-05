"""Декораторы"""

import sys
import logging
import logs.server_log_config
import logs.client_log_config
import traceback
import inspect


if sys.argv[0].find('client.py') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


def log(func_to_log):
    def log_decorator(*args, **kwargs):
        log_function = func_to_log(*args, **kwargs)
        LOGGER.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {func_to_log.__module__}.'
                     f'Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}.'
                     f'Вызов из функции {inspect.stack()[1][3]}')
        return log_function
    return log_decorator

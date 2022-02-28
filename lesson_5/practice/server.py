import json
import logging
import socket
import sys
import log.server_log_config

from common.variables import DEFAULT_PORT, MAX_CONNECTIONS, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR
from common.utils import get_message, send_message


server_logger = logging.getLogger('server')


def process_client_message(message):
    server_logger.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p')+1])
        else:
            listen_port = DEFAULT_PORT
            server_logger.warning(f'Сервер будет запущен с портом по умолчанию {listen_port}')
        if listen_port < 1024 or listen_port > 65535:
            server_logger.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                                   f'{listen_port}. Допустимы адреса с 1024 до 65535.')
            sys.exit(1)
    except IndexError:
        logging.error('Порт не задан, после параметра \'p\'')
        sys.exit(1)
    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''
    except IndexError:
        logging.error('Не указан адрес, который будет слушать сервер, после параметра \'a\'')
        sys.exit(1)
    server_logger.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес с которого принимаются подключения: {listen_address}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        server_logger.info(f'Установлено соедение с клиентом {client_address}')
        try:
            message_from_client = get_message(client)
            server_logger.debug(f'Получено сообщение {message_from_client}')
            response = process_client_message(message_from_client)
            server_logger.info(f'Сформирован ответ клиенту {response}')
            send_message(client, response)
            server_logger.debug(f'Соединение с клиентом {client_address} закрывается.')
            client.close()
        except json.JSONDecodeError:
            server_logger.error(f'Не удалось декодировать Json строку, полученную от '
                                f'клиента {client_address}. Соединение закрывается.')
            client.close()


if __name__ == '__main__':
    main()

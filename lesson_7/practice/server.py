import argparse
import json
import logging
import select
import socket
import sys
import time

import logs.server_log_config

from common.variables import DEFAULT_PORT, MAX_CONNECTIONS, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import get_message, send_message
from decorator import log


server_logger = logging.getLogger('server')


@log
def process_client_message(message, messages_list, client):
    server_logger.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if listen_port is None:
        logging.error('Порт не задан, после параметра \'p\'')
        sys.exit(1)

    if listen_port is None:
        logging.error('Не указан адрес, который будет слушать сервер, после параметра \'a\'')
        sys.exit(1)

    if not 1023 < listen_port < 65536:
        server_logger.critical(
            f'Попытка запуска сервера с указанием неподходящего порта '
            f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return listen_address, listen_port


def main():
    listen_address, listen_port = arg_parser()

    server_logger.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес с которого принимаются подключения: {listen_address}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)

    clients = []
    messages = []

    transport.listen(MAX_CONNECTIONS)

    while True:
        try:
            client, client_address = transport.accept()
        except OSError as err:
            server_logger.error(f'error number is {err.errno}, because it\'s just a timeout')
            pass
        else:
            server_logger.info(f'Установлено соединение с клиентом {client_address}')
            clients.append(client)

        recv_data = []
        send_data = []
        errors = []

        try:
            if clients:
                recv_data, send_data, errors = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data:
            for client_with_message in recv_data:
                try:
                    message_from_client = get_message(client_with_message)
                    process_client_message(message_from_client,
                                           messages, client_with_message)
                    server_logger.debug(f'Получено сообщение {message_from_client}')
                except:
                    server_logger.info(f'Клиент {client_with_message.getpeername()} '
                                       f'отключился от сервера.')
                    clients.remove(client_with_message)

        if messages and send_data:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            messages.pop(0)
            for waiting_client in send_data:
                try:
                    send_message(waiting_client, message)
                except:
                    server_logger.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()

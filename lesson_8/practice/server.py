import argparse
import logging
import select
import socket
import sys

import logs.server_log_config

from common.variables import DEFAULT_PORT, MAX_CONNECTIONS, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    ERROR, MESSAGE, MESSAGE_TEXT, SENDER, RESP_200, RESP_400, DESTINATION, EXIT_MESSAGE
from common.utils import get_message, send_message
from decorator import log


server_logger = logging.getLogger('server')


@log
def process_client_message(message, messages_list, client, clients, names):
    server_logger.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message:
        if message[USER][ACCOUNT_NAME] not in names:
            names[message[USER][ACCOUNT_NAME]] = client
            send_message(client, RESP_200)
        else:
            response = RESP_400
            response[ERROR] = 'Имя пользователя занято'
            send_message(client, response)
            clients.remove(client)
            client.close()
        return
    elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and \
            TIME in message and SENDER in message and MESSAGE_TEXT in message:
        messages_list.append(message)
        return
    elif ACTION in message and message[ACTION] == EXIT_MESSAGE and ACCOUNT_NAME in message:
        clients.remove(names[message[ACCOUNT_NAME]])
        names[message[ACCOUNT_NAME]].close()
        names.pop(message[ACCOUNT_NAME])
        return
    else:
        response = RESP_400
        response[ERROR] = 'Неверный запрос'
        send_message(client, response)
        return


@log
def process_message(message, names, listen_socks):
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        server_logger.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                           f'от пользователя {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        server_logger.error(
            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')


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

    names = dict()

    transport.listen(MAX_CONNECTIONS)

    while True:
        try:
            client, client_address = transport.accept()
        except OSError as err:
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
                    process_client_message(message_from_client, messages,
                                           client_with_message, clients, names)
                    server_logger.debug(f'Получено сообщение {message_from_client}')
                except Exception:
                    server_logger.info(f'Клиент {client_with_message.getpeername()} '
                                       f'отключился от сервера.')
                    clients.remove(client_with_message)

        for i in messages:
            try:
                process_message(i, names, send_data)
            except Exception:
                server_logger.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                clients.remove(names[i[DESTINATION]])
                names.pop(i[DESTINATION])
        messages.clear()


if __name__ == '__main__':
    main()

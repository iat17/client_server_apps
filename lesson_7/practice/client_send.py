import sys
import json
import socket
import time
import argparse
import logging
import logs.client_log_config
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, \
    ACTION, TIME, USER, ACCOUNT_NAME, SENDER, PRESENCE, RESPONSE, ERROR, MESSAGE, MESSAGE_TEXT, EXIT_MESSAGE
from common.utils import get_message, send_message
from decorator import log

# Инициализация клиентского логера
client_logger = logging.getLogger('client')


@log
def message_from_server(message):
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        client_logger.info(f'Получено сообщение от пользователя '
                    f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        client_logger.error(f'Получено некорректное сообщение с сервера: {message}')


@log
def create_message(sock, account_name='Guest'):
    message = input(f'Введите сообщение для отправки или \'{EXIT_MESSAGE}\' для завершения работы: ')
    if message == EXIT_MESSAGE:
        sock.close()
        client_logger.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    result_message = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    client_logger.debug(f'Сформирован словарь сообщения: {result_message}')
    return result_message


@log
def create_presence(account_name='Guest'):
    presence = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    client_logger.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return presence


@log
def process_ans(message):
    client_logger.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            return f'400 : {message[ERROR]}'
    raise ValueError


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if server_address is None:
        client_logger.error('Не задан адрес сервера после параметра \'addr\'')
        sys.exit(1)

    if server_port is None:
        client_logger.error('Не задан порт сервера после параметра \'port\'')
        sys.exit(1)

    if client_mode is None:
        client_logger.error('Не задан client mode после параметра \'-m\'')
        sys.exit(1)

    if not 1023 < server_port < 65536:
        client_logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    if client_mode not in ('listen', 'send'):
        client_logger.critical(f'Указан недопустимый режим работы {client_mode}, '
                               f'допустимые режимы: listen , send')
        sys.exit(1)

    return server_address, server_port, client_mode


def main():
    server_address, server_port, client_mode = arg_parser()

    client_logger.info(f'Запущен клиент с парамертами: адрес сервера: {server_address}, '
                       f'порт: {server_port}, режим работы {client_mode}')

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(transport, message_to_server)
        client_logger.info(f'Сообщение {message_to_server} отправлено')
        answer = process_ans(get_message(transport))
        client_logger.info(f'Принят ответ от сервера {answer}')
    except json.JSONDecodeError:
        client_logger.error('Ошибка декодирования Json.')
    except ConnectionRefusedError:
        client_logger.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                               f'конечный компьютер отверг запрос на подключение.')
    else:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            if client_mode == 'send':
                try:
                    send_message(transport, create_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    client_logger.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)
            if client_mode == 'listen':
                try:
                    message_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    client_logger.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)

if __name__ == '__main__':
    main()

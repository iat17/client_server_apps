import subprocess

import chardet

RESOURCE_YOUTUBE = 'youtube.ru'
RESOURCE_YANDEX = 'yandex.ru'

resources_list = [RESOURCE_YOUTUBE, RESOURCE_YANDEX]


def get_ping_result(resources: list) -> None:
    for resource in resources:
        args = ['ping', '-c', '2', resource]
        result = subprocess.Popen(args, stdout=subprocess.PIPE)
        for line in result.stdout:
            detected_encoding = chardet.detect(line)
            line = line.decode(detected_encoding['encoding']).encode('utf-8')
            print(line.decode('utf-8'))


get_ping_result(resources_list)

from typing import List

LIST_VALUES = ['разработка', 'администрирование', 'protocol', 'standard']


def get_bytes_and_return_back(values: List[str]) -> None:
    for value in values:
        byte_value = value.encode('utf-8')
        print(byte_value)
        str_value = byte_value.decode('utf-8')
        print(str_value)


get_bytes_and_return_back(LIST_VALUES)

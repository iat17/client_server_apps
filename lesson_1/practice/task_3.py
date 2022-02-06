LIST_VALUES = ['attribute', 'класс', 'функция', 'type']


def check_values(values: list) -> None:
    false_values = []
    for value in values:
        try:
            bytes(value, 'ascii')
        except UnicodeEncodeError:
            false_values.append(value)
    print(f'{false_values}: can not be written as bytes')


check_values(LIST_VALUES)

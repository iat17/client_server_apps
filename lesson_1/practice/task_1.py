FIRST_WORD_STR = 'разработка'
SECOND_WORD_STR = 'сокет'
THIRD_WORD_STR = 'декоратор'
FIRST_WORD_UNICODE = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
SECOND_WORD_UNICODE = '\u0441\u043e\u043a\u0435\u0442'
THIRD_WORD_UNICODE = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'

list_of_str = [FIRST_WORD_STR, SECOND_WORD_STR, THIRD_WORD_STR]
list_of_unicode = [FIRST_WORD_UNICODE, SECOND_WORD_UNICODE, THIRD_WORD_UNICODE]


def check_values(values: list) -> None:
    for value in values:
        print(value)
        print(type(value))


check_values(list_of_str)
check_values(list_of_unicode)

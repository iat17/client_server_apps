CLASS_BYTE = b'class'
FUNCTION_BYTE = b'function'
METHOD_BYTE = b'method'

bytes_list = [CLASS_BYTE, FUNCTION_BYTE, METHOD_BYTE]


def check_values(values: list) -> None:
    for value in values:
        print(type(value))
        print(value)
        print(len(value))


check_values(bytes_list)

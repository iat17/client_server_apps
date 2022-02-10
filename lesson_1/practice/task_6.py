import chardet

ROWS = ['сетевое программирование', 'сокет', 'декоратор']

with open('test_file.txt', 'w', encoding='utf-8') as f:
    for row in ROWS:
        f.write(row + '\n') if row != ROWS[-1] else f.write(row)

with open('test_file.txt', 'rb') as f:
    detected_encoding = chardet.detect(f.read())['encoding']

with open('test_file.txt', 'r', encoding=detected_encoding) as f:
    print(f.read())

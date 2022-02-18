import csv
import re

import chardet

files = ['info_1.txt', 'info_2.txt', 'info_3.txt']


def get_data(files: list):

    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = []

    for file in files:
        with open(file, 'rb') as file_bytes:
            unknown_encoding_data = file_bytes.read()
            detected_encoding = chardet.detect(unknown_encoding_data)
            data = unknown_encoding_data.decode(detected_encoding['encoding'])
        prod_reg = re.compile(r'Изготовитель системы:\s*\S*')
        name_reg = re.compile(r'Название ОС:\s*\S*')
        code_reg = re.compile(r'Код продукта:\s*\S*')
        type_reg = re.compile(r'Тип системы:\s*\S*')
        os_prod_list.append(prod_reg.findall(data)[0].split()[2])
        os_name_list.append(name_reg.findall(data)[0].split()[2])
        os_code_list.append(code_reg.findall(data)[0].split()[2])
        os_type_list.append(type_reg.findall(data)[0].split()[2])

    titles = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data.append(titles)

    grouped_data = [os_prod_list, os_name_list, os_code_list, os_type_list]

    count_rows = len(os_prod_list)

    for row in range(count_rows):
        result_line = [line[row] for line in grouped_data]
        main_data.append(result_line)

    return main_data


def write_to_csv(result_file):
    """Write the data to csv-file"""

    main_data = get_data(files)
    with open(result_file, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in main_data:
            writer.writerow(row)


write_to_csv('result.csv')




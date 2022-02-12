import yaml

LIST_DATA = {
    'array': ['1', '2', '3'],
    'integer': 10,
    'dictionary': {
        'not_ascii_1': 'Ё',
        'not_ascii_2': 'Б',
        'not_ascii_3': 'Ж'
    }
}

with open('file.yaml', 'w', encoding='utf-8') as f_w:
    yaml.dump(LIST_DATA, f_w, default_flow_style=False, allow_unicode=True)

with open('file.yaml', 'r', encoding='utf-8') as f_r:
    yaml_data = yaml.load(f_r, Loader=yaml.SafeLoader)

print(yaml_data == LIST_DATA)

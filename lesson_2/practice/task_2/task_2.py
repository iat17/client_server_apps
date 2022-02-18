import json


def write_order_to_json(item: str, quantity: str, price: str, buyer: str, date: str) -> None:

    with open('orders.json', 'r', encoding='utf-8') as file_r:
        data = json.load(file_r)
        orders = data['orders']
        order = {
            'item': item,
            'quantity': quantity,
            'price': price,
            'buyer': buyer,
            'date': date
        }
        orders.append(order)

    with open('orders.json', 'w', encoding='utf-8') as file_w:
        json.dump(data, file_w, indent=4)


write_order_to_json('laptop', '10', '73000', 'Алексеев И. И.', '01.01.2021')

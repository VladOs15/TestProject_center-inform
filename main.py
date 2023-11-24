import os
import random
from faker import Faker
import xeger
from xml.etree.ElementTree import Element, SubElement, ElementTree


def random_string(min_value, max_value):
    # length = random.randint(min_value, max_value)
    # letters_and_numbers = string.ascii_letters + string.digits
    # return ''.join(random.choice(letters_and_numbers) for _ in range(length))
    regex_pattern = f'[a-zA-Z0-9]{{{min_value},{max_value}}}'
    return xeger.xeger(regex_pattern)

# print(random_string(5,10))

def get_random_string_from_file(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        return random.choice(lines).strip()


# print(get_random_string_from_file('EAN.txt'))

def random_price():
    return round(random.uniform(100.00, 1000.00), 2)


# print(random_price())

def random_volume():
    step = 0.05
    return round(random.uniform(0.1, 3.0) // step * step, 4)


# print(random_volume())

def random_int(min_value, max_value):
    return random.randint(min_value, max_value)


# print(random_int(100,1000))

def random_ru_str(min_value, max_value):
    # ru_char = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя '
    # lenght = random.randint(min_value, max_value)
    # return ''.join(random.choice(ru_char) for _ in range(lenght))
    regex_pattern = f'[а-яА-Я ]{{{min_value},{max_value}}}'
    return xeger.xeger(regex_pattern)


# print(random_ru_str(5,10))

def random_date():
    # return f'{random_int(1, 31):02d}.{random_int(1, 12):02d}.{random_int(2015, 2023):04d} {random_int(0, 23):02d}:{random_int(0, 59):02d}:{random_int(0, 59):02d}'
    return Faker().date_of_birth()

# print(random_date())

def create_xml_file(xsdf):
    with open(xsdf, 'r') as xsd_file:
        xsd_shema = xsd_file.read()

    root = Element('Cheque')
    root.set('inn', get_random_string_from_file('INN.txt'))
    root.set('kpp', str(random_int(100000000, 999999999)))
    root.set('address', random_ru_str(20, 100))
    root.set('name', random_ru_str(10, 20))
    root.set('kassa', random_string(6, 12))
    root.set('shift', str(random_int(1, 100)))
    root.set('number', str(random_int(1, 100)))
    root.set('datetime', str(random_date()))

    for _ in range(random.randint(1, 10)):
        bottle = SubElement(root, 'Bottle')
        bottle.set('price', str(random_price()))
        bottle.set('barcode', random_string(50, 70))
        bottle.set('ean', get_random_string_from_file('EAN.txt'))
        bottle.set('volume', str(random_volume()))

    tree = ElementTree(root)
    xml_file = 'cheque.xml'
    tree.write(xml_file)

    return xml_file


def send_xml_file(xml_file):
    url = 'http://localhost:8000/xml'
    start_server = 'python -m http.server'
    command = f'curl -F "xml_file=@{xml_file}" {url}'
    os.system(start_server)
    os.system(command)



def main():
    xml_file = create_xml_file('xsd-схема.xsd')
    send_xml_file(xml_file)


if __name__ == "__main__":
    main()

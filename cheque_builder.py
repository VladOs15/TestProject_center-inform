import random
from xml.etree.ElementTree import Element, SubElement, ElementTree
import xeger


class ChequeBuilder:
    def __init__(self, xsd_shema, faker):
        self.xsd_shema = xsd_shema
        self.root = Element('Cheque')
        self.fake = faker

    @staticmethod
    def random_string(min_value, max_value):
        regex_pattern = f'[a-zA-Z0-9]{{{min_value},{max_value}}}'
        return xeger.xeger(regex_pattern)

    def get_random_string_from_file(self, file_name):
        with open(file_name, 'r') as file:
            lines = file.readlines()
            return random.choice(lines).strip()

    def random_price(self):
        return round(random.uniform(100.00, 1000.00), 2)

    def random_volume(self):
        step = 0.05
        return round(random.uniform(0.1, 3.0) // step * step, 4)

    def random_int(self, min_value, max_value):
        return random.randint(min_value, max_value)

    def generate_barcode(self):
        return xeger.xeger(r'\d\dN\w{20}\d[0-1]\d[0-3]\d{10}\w{31}')

    def generate_kpp(self):
        return xeger.xeger(r'\d{9}|')

    def random_ru_str(self, min_value, max_value):
        regex_pattern = f'[а-яА-Я ]{{{min_value},{max_value}}}'
        return xeger.xeger(regex_pattern)

    def random_date(self):
        # return xeger.xeger(r'[0-3][0-9][0-1][0-9][0-9]{2}[0-2][0-9][0-5][0-9]')
        return self.fake.date_of_birth()

    def create_xml_file(self):
        self.root.set('inn', self.get_random_string_from_file('INN.txt'))
        self.root.set('kpp', str(self.generate_kpp()))
        self.root.set('address', self.random_ru_str(20, 100))
        self.root.set('name', self.random_ru_str(10, 20))
        self.root.set('kassa', self.random_string(6, 12))
        self.root.set('shift', str(self.random_int(1, 100)))
        self.root.set('number', str(self.random_int(1, 100)))
        self.root.set('datetime', str(self.random_date()))

        for _ in range(random.randint(1, 10)):
            bottle = SubElement(self.root, 'Bottle')
            bottle.set('price', str(self.random_price()))
            bottle.set('barcode', self.generate_barcode())
            bottle.set('ean', self.get_random_string_from_file('EAN.txt'))
            bottle.set('volume', str(self.random_volume()))

    def save_cheque(self, file_path):
        tree = ElementTree(self.root)
        tree.write(file_path)

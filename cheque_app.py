from faker import Faker
from flask import Flask, request, send_file
from cheque_builder import ChequeBuilder

from xmlschema import XMLSchema

app = Flask(__name__)


class ChequeApp:
    def __init__(self, cheque_builder):
        self.cheque_builder = cheque_builder


@app.route('/xml', methods=['POST'])
def save_xml():
    file = request.files['xml_file']

    temp_filename = 'temp_cheque.xml'
    file.save(temp_filename)

    schema = XMLSchema('xsd-схема.xsd')
    with open(temp_filename, 'r', encoding='utf-8') as f:
        xml_file = f.read()

    if not schema.is_valid(xml_file):
        return 'File is broken\n'

    return 'File saved and sent successfully.\n'


@app.route('/xml', methods=['GET'])
def get_xml():
    return send_file('cheque.xml')


@app.route('/')
def index():
    return 'Welcome to Cheque App!'


if __name__ == "__main__":
    faker = Faker()
    cheque_builder = ChequeBuilder(faker)
    cheque_builder.create_xml_file()
    cheque_builder.save_cheque('cheque.xml')

    cheque_app = ChequeApp(cheque_builder)
    app.run(host='localhost', port=8080)

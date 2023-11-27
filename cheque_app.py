import subprocess

import requests
from faker import Faker
from flask import Flask, request, send_file
from cheque_builder import ChequeBuilder

app = Flask(__name__)


class ChequeApp:
    def __init__(self, cheque_builder):
        self.cheque_builder = cheque_builder


@app.route('/xml', methods=['POST'])
def save_xml():
    file = request.files['xml_file']

    temp_filename = 'temp_cheque.xml'
    file.save(temp_filename)

    try:
        subprocess.run(['xmllint', '--shema', 'xsd-схема.xsd', temp_filename, '--noout'], check=True)
    except subprocess.CalledProcessError:
        return 'Error: File XML invalid'

    file.save('cheque.xml')

    try:
        requests.post('http"//localhost:8080/xml', files={'xml_file': open('cheque.xml', 'rb')})
    except request.exceptions.RequestException as e:
        return f'Error sending XML file: {e}'

    return 'File saved and sent successfully.'


@app.route('/xml', methods=['GET'])
def get_xml():
    return send_file('cheque.xml', as_attachment=True)


@app.route('/')
def index():
    return 'Welcome to Cheque App!'


if __name__ == "__main__":
    with open('xsd-схема.xsd', 'r') as xsd_file:
        xsd_shema = xsd_file.read()

    faker = Faker()
    cheque_builder = ChequeBuilder(xsd_shema, faker)
    cheque_builder.create_xml_file()
    cheque_builder.save_cheque('cheque.xml')

    cheque_app = ChequeApp(cheque_builder)
    # app.add_url_rule('/xml', 'save_xml', save_xml, methods=['POST'])
    # app.add_url_rule('/xml', 'get_xml', get_xml, methods=['GET'])
    # app.add_url_rule('/', 'index', index)
    app.run(host='localhost', port=8080)

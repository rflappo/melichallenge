import os

import threading

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from config import config
from api_client import MeliApiClient


app = Flask('__melichallenge__')
config(app)

db = SQLAlchemy(app)


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, nullable=False)
    site = db.Column(db.String(length=16), nullable=False)
    price = db.Column(db.Float)
    start_time = db.Column(db.DateTime)
    name = db.Column(db.String(length=128))
    description = db.Column(db.String(length=64))
    nickname = db.Column(db.String(length=50))

    __table_args__ = (
        db.PrimaryKeyConstraint('site', 'id'),
        {}
    )

    def __str__(self):
        return f"<Item id:{self.id}"\
               f", site:{self.site}"\
               f", price:{self.price}"\
               f", name:{self.name}"\
               f", description:{self.description}"\
               f", nickname:{self.nickname}"


class FileHandler():
    def __init__(self, path_to_file):
        self.client = MeliApiClient()
        self.ext = os.path.split(path_to_file)[-1].split('.')[-1].lower()
        self.encoding = 'utf-8'
        self.separator = ','
        self.delimiter = "\r\n"
        self.headers = True
        self.path_to_file = path_to_file

    def _get_and_set_item_currency(self, currency_id):
        currency_data = self.client.get_currency(currency_id)
        if currency_data.get('error') is None:
            return currency_data['description']

    def _get_and_set_item_seller(self, seller_id):
        seller_data = self.client.get_user(seller_id)
        if seller_data.get('error') is None:
            return seller_data.get('nickname')

    def _get_and_set_item_category(self, category_id):
        category_data = self.client.get_category(category_id)
        if category_data.get('error') is None:
            return category_data.get('name')

    def _process_item(self, id, site, item_data):
        item = Item()
        item.id, item.site = id, site

        item.price = item_data.get('price')
        item.start_time = item_data.get('start_time')

        currency_id = item_data.get('currency_id', '-1')
        item.description = self._get_and_set_item_currency(currency_id)

        seller_id = item_data.get('seller_id', '-1')

        item.nickname = self._get_and_set_item_seller(seller_id)

        category_id = item_data.get('category_id', '-1')
        item.name = self._get_and_set_item_category(category_id)

        print(str(item))

    def _process_line(self, line, labels=None):
        data = line.strip(self.delimiter).split(self.separator)
        site, id = data if labels[0] == 'site' else data[::-1]

        item_data = self.client.get_item(f"{site}{id}")
        if item_data.get('error') is None:
            self._process_item(id, site, item_data)

    def process_file(self):
        with open(self.path_to_file, 'r', encoding=self.encoding) as data_file:
            if self.ext not in ['jsonl']:
                labels = data_file.readline().split(self.separator)
                for line in data_file:
                    self._process_line(line, labels=labels)


def uploader():

    if 'file' not in request.files:
        return jsonify({'BadRequest': 'Please send a file'}), 400

    filename = secure_filename(request.files['file'].filename)
    path_to_file = os.path.join(os.getcwd(), filename)
    request.files['file'].save(path_to_file)

    handler = FileHandler(path_to_file)
    handler.process_file()

    return jsonify({'message': 'File uploaded successfully'}), 200


app.add_url_rule("/uploader", view_func=uploader, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)

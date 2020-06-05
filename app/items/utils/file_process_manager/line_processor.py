from app.services.api_client import MeliApiClient
from app.model import Item
from app.data import db
from sqlalchemy.orm import sessionmaker

import os
from configparser import ConfigParser


class LineParserConfig:
    def __init__(self):
        config = ConfigParser()
        config_file = os.path.join(os.getcwd(), 'parserconfig.ini')
        config.read(config_file)

        self.settings = {}
        if 'LINE' in config.sections():
            self.settings = config['LINE']
    
    def get_line_feed(self):
        line_feed = '\n'

        is_there = 'LINE_FEED' in self.settings.keys()
        if is_there and self.settings['LINE_FEED'].lower() != 'unix':
            line_feed == '\r\n'
        
        return line_feed

    def get_separator(self):
        if 'SEPARATOR' in self.settings.keys():
            return self.settings['SEPARATOR']
        return ','

    def get_parse_module(self):
        parse_module = None

        is_there = 'MODULE' in self.settings.keys()
        if is_there and self.settings['MODULE'].lower() != 'none':
            parse_module = self.settings['MODULE']

        return parse_module
    
    def get_parse_method(self):
        parse_method = None

        is_there = 'METHOD' in self.settings.keys()
        if is_there and self.settings['METHOD'].lower() != 'none':
            parse_method = self.settings['METHOD'].lower()

        return parse_method


class LineProcessor():
    def __init__(self, line, encoding, header_line=None):
        self.config = LineParserConfig()

        Session = sessionmaker(bind=db.get_engine())
        self.db_session = Session()

        self.client = MeliApiClient()

        self.header_line = self._clean_line(header_line) if header_line else header_line
        self.line = line.decode(encoding)

    def _clean_line(self, line):
        return line.strip(self.config.get_line_feed())
    
    def _parse_line(self):
        data = None

        line = self._clean_line(self.line)

        parse_method = self.config.get_parse_method()
        if parse_method:
            parse_module = self.config.get_parse_module()
            if parse_module:
                method = getattr(__import__(parse_module), parse_method)
                data = method(line)
            else:
                data = eval(parse_method)(line)
        else:
            # If there is NO header_line I should abort (I have no clue how to interpret it)
            headers = self.header_line.split(self.config.get_separator())
            line_data = line.split(self.config.get_separator())
            data = {key: val for key, val in zip(headers, line_data)}

        return data

    def _get_and_set_item_currency(self, currency_id, item):
        currency_data = self.client.get_currency(currency_id)
        if currency_data.get('error') is None:
            item.description = currency_data['description']

    def _get_and_set_item_seller(self, seller_id, item):
        seller_data = self.client.get_user(seller_id)
        if seller_data.get('error') is None:
            item.nickname = seller_data.get('nickname')

    def _get_and_set_item_category(self, category_id, item):
        category_data = self.client.get_category(category_id)
        if category_data.get('error') is None:
            item.name = category_data.get('name')

    def _seed_item_from_api(self, item):
        from_api = self.client.get_item(f"{item.site}{item.id}")
        if from_api.get('error') is None:
            item.price = from_api.get('price')
            item.start_time = from_api.get('start_time')

            args = [
                from_api.get('currency_id', '-1'),
                from_api.get('seller_id', '-1'),
                from_api.get('category_id', '-1')
            ]

            funcs = [
                self._get_and_set_item_currency,
                self._get_and_set_item_seller,
                self._get_and_set_item_category
            ]

            for fn, arg in zip(funcs, args):
                fn(arg, item)

            self.db_session.merge(item)
            self.db_session.commit()

    def _process_item_data(self, item_data):
        item_site = item_data.get('site')
        item_site = item_site if item_site else None

        item_id = item_data.get('id')

        item = Item.get_or_create_item(
            site=item_site,
            id=item_id,
            db_session=self.db_session
        )

        if item:
            self._seed_item_from_api(item)

    def process_line(self):
        data = self._parse_line()

        self._process_item_data(data)
        
        self.db_session.close()

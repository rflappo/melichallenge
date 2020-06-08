from app.services.api_client import MeliApiClient
from app.model import Item
from app.data import db
from sqlalchemy.orm import sessionmaker


class LineProcessor():
    def __init__(self, line, line_parser, header_line=None):
        self.config = line_parser

        Session = sessionmaker(bind=db.get_engine())
        self.db_session = Session()

        self.client = MeliApiClient()

        self.header_line = self._clean_line(header_line) if header_line else header_line
        self.line = line.decode(self.config.get_parse_encoding())

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
        value = None
        if currency_data.get('error') is None:
            value = currency_data.get('description')
        item.description = value

    def _get_and_set_item_seller(self, seller_id, item):
        seller_data = self.client.get_user(seller_id)
        value = None
        if seller_data.get('error') is None:
            value = seller_data.get('nickname')
        item.nickname = value

    def _get_and_set_item_category(self, category_id, item):
        category_data = self.client.get_category(category_id)
        value = None
        if category_data.get('error') is None:
            value = category_data.get('name')
        item.name = value

    def _seed_item_from_api(self, from_api, item):
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

        from_api = self.client.get_item(f"{item_site}{item_id}")
        if from_api.get('error') is None:

            item = Item.get_or_create_item(
                site=item_site,
                id=item_id,
                db_session=self.db_session
            )

            if item:
                self._seed_item_from_api(from_api, item)

    def process_line(self):
        data = self._parse_line()

        self._process_item_data(data)
        
        self.db_session.close()

from app.services.api_client import MeliApiClient
from app.model import Item
from app.data import db
from sqlalchemy.orm import sessionmaker


class LineProcessor():
    def __init__(self, line):
        Session = sessionmaker(bind=db.get_engine())
        self.db_session = Session()

        self.client = MeliApiClient()

        self.line = line.decode('utf-8')

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

    def process_line(self):
        site, id = self.line.strip('\r\n').split(',')
        self.item = Item.get_or_create_item(site=site, id=id, db_session=self.db_session)

        item_data = self.client.get_item(f"{self.item.site}{self.item.id}")
        if item_data.get('error') is None:
            self.item.price = item_data.get('price')
            self.item.start_time = item_data.get('start_time')

            currency_id = item_data.get('currency_id', '-1')
            self.item.description = self._get_and_set_item_currency(currency_id)

            seller_id = item_data.get('seller_id', '-1')
            self.item.nickname = self._get_and_set_item_seller(seller_id)

            category_id = item_data.get('category_id', '-1')
            self.item.name = self._get_and_set_item_category(category_id)

            self.db_session.merge(self.item)
            self.db_session.commit()
        
        self.db_session.close()

    def __str__(self):
        return str(self.item)

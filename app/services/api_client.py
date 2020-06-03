import requests
from urllib.parse import urljoin


class MeliApiClient:
    ''' API client for MeLi REST API '''
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://api.mercadolibre.com"  # Should parametrize

    def _get_data(self, url_suffix, **kwargs):
        """Make request to SL to GET data.."""
        full_url = urljoin(self.base_url, url_suffix)
        response = self.session.get(full_url)
        return response.json()

    @staticmethod
    def _get_rest_suffix(resource_suffix, element_id):
        return f"{resource_suffix}/{element_id}"

    def get_item(self, item_id):
        url_suffix = self._get_rest_suffix("items", item_id)
        return self._get_data(url_suffix)

    def get_currency(self, currency_id):
        url_suffix = self._get_rest_suffix("currencies", currency_id)
        return self._get_data(url_suffix)

    def get_user(self, user_id):
        url_suffix = self._get_rest_suffix("users", user_id)
        return self._get_data(url_suffix)

    def get_category(self, category_id):
        url_suffix = self._get_rest_suffix("categories", category_id)
        return self._get_data(url_suffix)

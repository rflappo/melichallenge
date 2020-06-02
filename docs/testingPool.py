from itertools import chain
from api_client import MeliApiClient
from time import perf_counter, sleep, perf_counter
from multiprocessing import Process, Manager, cpu_count


class SpawnProcess():
    def __init__(self, line):
        self.client = MeliApiClient()
        self.site, self.id = line.strip('\r\n').split(',')

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

    def work(self):
        item_data = self.client.get_item(f"{self.site}{self.id}")

        self.price = item_data.get('price')
        self.start_time = item_data.get('start_time')

        currency_id = item_data.get('currency_id', '-1')
        self.description = self._get_and_set_item_currency(currency_id)

        seller_id = item_data.get('seller_id', '-1')
        self.nickname = self._get_and_set_item_seller(seller_id)

        category_id = item_data.get('category_id', '-1')
        self.name = self._get_and_set_item_category(category_id)

    def __str__(self):
        return f"<Item id:{self.id}"\
               f", site:{self.site}"\
               f", price:{self.price}"\
               f", name:{self.name}"\
               f", description:{self.description}"\
               f", nickname:{self.nickname}"


def queued_work(in_queue):
    while True:
        line = in_queue.get()

        # exit signal
        if line:
            new_process = SpawnProcess(line)
            new_process.work()
            print(new_process)
        else:
            return
        # fake work


if __name__ == "__main__":
    num_workers = cpu_count()

    manager = Manager()

    args_queue = manager.Queue(num_workers)

    start = perf_counter()
    # start for workers    
    pool = []
    for i in range(num_workers):
        p = Process(target=queued_work, args=(args_queue,))
        p.start()
        pool.append(p)

    # produce data
    with open("technical_challenge_data.csv") as f:
        iters = chain(f, (None,)*num_workers)

        for line in iters:
            args_queue.put(line)

    for p in pool:
        p.join()

    end = perf_counter()
    print(end - start)
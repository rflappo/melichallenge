import time
import asyncio
from itertools import groupby
from collections import defaultdict

import aiohttp  # tenes que instalarlo a este
import requests


session = requests.Session()
base_url = "https://api.mercadolibre.com"  # Should parametrize


async def _get_items(session, data_file):

    aws = []

    grouped = groupby(
        sorted(data_file, key=lambda x: x[:x.index(',')]),
        key=lambda x: x[:x.index(',')]
    )

    for country, lines in grouped:

        print(f'PROCESSING {country}')

        if country == '':
            continue

        # aa = set([line.replace(",", "").replace("\n", "") for line in lines])
        processed_lines = set([])
        for line in lines:

            item_id = line.replace(",", "").replace("\n", "")

            if item_id in processed_lines:
                continue

            processed_lines.add(item_id)
            # TODO: move to method
            url = f'{base_url}/items/{item_id}'
            aws.append(session.get(url))

    responses = [await response.json()
                 for response in (await asyncio.gather(*aws))
                 if response.status == 200]
    return responses


async def _process_items(session, items):

    to_process = {
        'currencies': 'currency_id',
        'sellers': 'seller_id',
        'categories': 'category_id'
    }

    collector = defaultdict(set)

    for item in items:

        for k, _id in to_process.items():

            if _id in item:
                collector[k].add(session.get(f'{base_url}/{k}/{item[_id]}'))

    # responses = {
    #     group_key: [await response.json()
    #                 for response in (await asyncio.gather(*requests))
    #                 if response.status == 200]
    #     for group_key, requests in collector.items()
    # }

    data = defaultdict(dict)

    for group_key, requests in collector.items():

        for response in (await asyncio.gather(*requests)):

            if response.status != 200:
                continue

            resp = await response.json()
            data[group_key][resp['id']] = resp

    return data


def _create_items(items, items_data):

    for item in items:

        category_id = item.get('category_id')
        if category_id is not None:
            item['category_name'] = items_data['categories'][category_id].get('name', 'Not specified')

        currency_id = item.get('currency_id')
        if currency_id is not None:
            item['currency_description'] = items_data['currencies'][currency_id].get('desription', 'Not specified')

    return items


with open('technical_challenge_data.txt', 'r',
          encoding='utf-8') as data_file:

    labels = data_file.readline().split(',')

    async def requests_by_country(grouped):

        async with aiohttp.ClientSession() as session:

            items = await _get_items(session, data_file)

            items_data = await _process_items(session, items)

            items_to_save = _create_items(items, items_data)
            # print(items_data)

    start = time.time()

    coro = requests_by_country(data_file)
    asyncio.run(coro)
    end = time.time()
    print(f'TOOK: {end - start}')
    print()
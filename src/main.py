import asyncio
import json
import httpx
import math
from pprint import pprint
from httpx import Timeout

from logger import get_logger

logger = get_logger('main', 'txbit', 'depth')

REQUEST_TIMEOUT = 30
async def get_depth(pair:str, direction:str):
    url = f'https://api.txbit.io/api/public/getorderbook?market={pair}&type={direction}'

    async with httpx.AsyncClient(timeout=Timeout(REQUEST_TIMEOUT)) as client:
        response = await client.get(url)
    
    if response.status_code != 200:
        logger.error(f'{response.status_code} {url}')
        return None
    
    data = json.loads(response.text)
    return data


async def get_markets():
    url = 'https://api.txbit.io/api/public/getmarkets'

    async with httpx.AsyncClient(timeout=Timeout(REQUEST_TIMEOUT)) as client:
        response = await client.get(url)
    
    if response.status_code != 200:
        logger.error(f'{response.status_code} {url}')
        return None
    
    data = json.loads(response.text)
    return data

def calc_usdt(data):
    # print('\ncalc_usdt')
    # for i in data:
    #     print(i)
    vals = [val['Quantity'] * val['Rate'] for val in data]
    # for i in vals:
    #     print(round(i, 8))
    return sum(vals)


async def main():
    deepness = 10
    # markets = await get_markets()
    # pprint(markets)
    depth = await get_depth('AVN/USDT', 'both')
    if depth['success']:
        sell = depth['result']['sell']
        buy = depth['result']['buy']

        print('Total')
        sell_l = [val['Quantity'] for val in sell]
        usdt = calc_usdt(sell)
        print(f'sellers {len(sell)} AVN={sum(sell_l)} usdt={round(usdt)}')

        buy_l = [val['Quantity'] for val in buy]
        usdt = calc_usdt(buy)
        print(f'buyers  {len(buy)} AVN={sum(buy_l)} usdt={round(usdt)}')

        sell_l = sell_l[-deepness:]
        usdt_b = calc_usdt(sell[-deepness:])

        buy_l = buy_l[:deepness]
        usdt_s = calc_usdt(buy[:deepness])
        
        print()
        print(f'depth={deepness}')
        print(f'sellers AVN={sum(sell_l)} usdt={round(usdt_b)}')
        print(f'buyers  AVN={sum(buy_l)} usdt={round(usdt_s)}')
        
        print()
        print(f'sell')
        for i in sell[-deepness:]:
            print(f'{i}')

        print(f'buy')
        for i in buy[:deepness]:
            print(f'{i}')


print('-')
# if __name__ == 'main':
    # print('0')
    # ioloop = asyncio.get_event_loop()
    # tasks = [
    #     ioloop.create_task(main()), 
    # ]
    # wait_tasks = asyncio.wait(tasks)
    # print('1')
    # ioloop.run_until_complete(wait_tasks)

ioloop = asyncio.get_event_loop()
tasks = [
    ioloop.create_task(main()), 
]
wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)

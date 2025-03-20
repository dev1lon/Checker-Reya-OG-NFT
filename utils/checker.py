import asyncio
import aiohttp
from aiohttp_proxy import ProxyConnector
from fake_useragent import UserAgent

from utils import logger


logger = logger.get_logger()


async def checker(address, proxy, semaphore):
    async with semaphore:
        connector = ProxyConnector.from_url(f'http://{proxy}')
        headers = {
            'accept': 'application/json, text/plain, */*',
            'origin': 'https://app.reya.xyz',
            'priority': 'u=1, i',
            'referer': 'https://app.reya.xyz/',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-gpc': '1',
            'user-agent': UserAgent().random
        }

        async with aiohttp.ClientSession(connector=connector) as session:
            for attempt in range(0, 3):
                try:
                        async with session.get(url=f'https://api.reya.xyz/api/sbt/mint-status/owner/{address}/tokenCount/0', headers=headers) as response:
                            data = await response.json()
                            if data['isEligible'] == True:
                                eligible = 'Eligible'
                                if data['hasMinted'] == True:
                                    minted = 'NFT alredy minted'
                                else:
                                    minted = 'Can mint'
                                logger.success(f"{address} | {eligible} | {minted}")
                            else:
                                eligible = 'Not eligible'
                                logger.success(f"{address} | {eligible}")
                            await asyncio.sleep(1)
                            return

                except Exception as err:
                    logger.warning(f'{address} | {err} |  Retry')
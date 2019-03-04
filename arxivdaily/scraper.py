import asyncio
import logging
import time
from typing import Dict, Tuple

import aiohttp

from . import config

config.configure_logging()

log = logging.getLogger(__name__)


async def _get_pages() -> Dict[str, str]:
    log.debug('Reading pages.')
    connector = aiohttp.TCPConnector(limit=config.MAX_CONNECTIONS)
    timeout = aiohttp.ClientTimeout(total=config.HTTP_TIMEOUT)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:

        async def get_page(category: str) -> Tuple[str, str]:
            log.debug('Requesting URL for %s.', category)
            url = config.HTML_URL_TEMPLATE_MINIMAL.format(category=category)
            async with session.get(url) as response:
                assert response.status == 200
                return category, await response.text()

        awaitables = (get_page(category) for category in config.CATEGORIES)
        log.debug('Reading page texts.')
        time_start = time.monotonic()
        pages = dict(await asyncio.gather(*awaitables))

    log.debug('Read %s pages in %.1fs.', len(pages), time.monotonic() - time_start)
    pages = {category: pages[category] for category in config.CATEGORIES}
    return pages


def get_pages() -> Dict[str, str]:
    log.debug('Reading pages.')
    time_start = time.monotonic()
    pages = asyncio.run(_get_pages(), debug=True)
    log.info('Read %s pages in %.1fs.', len(pages), time.monotonic() - time_start)
    return pages


if __name__ == '__main__':
    print(get_pages().keys())

import asyncio
import logging
from typing import Dict, List

import aiohttp

from arxivdaily import config

config.configure_logging()

log = logging.getLogger(__name__)


async def _get_pages(urls: List[str]) -> Dict[str, bytes]:
    log.debug('Getting pages for %s URLs.', len(urls))
    # conn = aiohttp.TCPConnector(limit=config.MAX_CONNECTIONS)
    timeout = aiohttp.ClientTimeout(total=config.HTTP_TIMEOUT)
    pages = {}
    async with aiohttp.ClientSession(timeout=timeout) as session:
        for url in urls:
            log.debug('Getting page for URL %s', url)
            async with session.get(url) as resp:
                assert resp.status == 200
                pages[url] = await resp.text()
            log.debug('Got page for URL %s', url)
    return pages


def get_pages() -> Dict[str, bytes]:
    log.debug('Getting pages.')
    urls = [config.HTML_URL_TEMPLATE_MINIMAL.format(category=category) for category in config.CATEGORIES]
    return asyncio.run(_get_pages(urls))


if __name__ == '__main__':
    print(get_pages().keys())

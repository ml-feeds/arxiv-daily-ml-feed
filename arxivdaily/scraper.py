import asyncio
import logging
from typing import Dict

import aiohttp

from arxivdaily import config

config.configure_logging()

log = logging.getLogger(__name__)


async def _get_pages() -> Dict[str, str]:
    log.debug('Getting pages.')
    tasks = {}
    pages = {}
    # conn = aiohttp.TCPConnector(limit=config.MAX_CONNECTIONS)
    timeout = aiohttp.ClientTimeout(total=config.HTTP_TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as session:

        async def get_page(url: str) -> str:
            log.debug('Getting page for URL %s', url)
            async with session.get(url) as resp:
                assert resp.status == 200
                return await resp.text()

        for category in config.CATEGORIES:
            url = config.HTML_URL_TEMPLATE_MINIMAL.format(category=category)
            tasks[category] = asyncio.create_task(get_page(url))
            log.debug('Created task for %s.', category)
        for category in config.CATEGORIES:
            pages[category] = await tasks[category]
            log.debug('Got page for %s having size %s.', category, len(pages[category]))
    return pages


def get_pages() -> Dict[str, str]:
    log.debug('Getting pages.')
    pages = asyncio.run(_get_pages(), debug=True)
    log.debug('Got pages.')
    return pages


if __name__ == '__main__':
    print(get_pages().keys())

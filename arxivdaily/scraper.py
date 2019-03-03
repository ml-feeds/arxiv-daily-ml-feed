import asyncio
import logging
from typing import Dict

import aiohttp

from . import config

config.configure_logging()

log = logging.getLogger(__name__)


def pages() -> Dict[str, bytes]:
    pass

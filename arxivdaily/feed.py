import datetime
from functools import lru_cache
from json import dumps, loads
import logging

from cachetools.func import ttl_cache
from dateutil.parser import parse as parse_date
from feedgen.feed import FeedGenerator
from hext import Html, Rule
from humanize import naturalsize

from . import config
from .scraper import get_pages

config.configure_logging()

log = logging.getLogger(__name__)


class Feed:
    def __init__(self):
        self._hext_rule_extract = Rule(config.HTML_HEXT).extract

    @staticmethod
    def _init_feed() -> FeedGenerator:
        feed = FeedGenerator()
        feed.title(config.FEED_TITLE)
        feed.link(href=config.REPO_URL, rel='self')
        feed.description(config.FEED_DESCRIPTION)
        return feed

    @lru_cache(maxsize=1)
    def _output(self, pages: str) -> bytes:
        pages = loads(pages)
        pages = {category: self._hext_rule_extract(Html(text))[0] for category, text in pages.items()}

        feed = self._init_feed()
        # stat.ML: 47 new entries for Thu, 28 Feb 2019 | https://arxiv.org/list/stat.ML/recent#2019-02-28
        for category, item in pages.items():
            entry = feed.add_entry(order='append')
            num_entries = 0
            date_ = item["date"][0]
            title = f'{category}: {num_entries} new entries for {date_}'
            link = f'{config.HTML_URL_TEMPLATE_RECENT.format(category=category)}#{parse_date(date_).date()}'
            entry.title(title)
            entry.link(href=link)
            entry.guid(link, permalink=False)
            log.debug('Added feed item "%s" having link %s', title, link)

        text_: bytes = feed.rss_str(pretty=True)
        log.info('XML output has %s items.', text_.count(b'<item>'))
        return text_

    @ttl_cache(maxsize=1, ttl=config.CACHE_TTL)
    def feed(self) -> bytes:
        log.debug('Reading HTML.')
        texts = get_pages()
        texts = dumps(texts)  # Hashable (for caching)
        log.debug('Read HTML.')
        text = self._output(texts)
        log.info('XML output has size %s.', humanize_len(text))
        return text


def humanize_len(text: bytes) -> str:
    return naturalsize(len(text), gnu=True, format='%.0f')

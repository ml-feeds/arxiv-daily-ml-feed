from functools import lru_cache
from json import dumps, loads
import logging
from re import fullmatch
from urllib.parse import parse_qs, urlparse

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
        for category, item in pages.items():
            entry = feed.add_entry(order='append')

            url_having_count = urlparse(item['link'][1])
            if parse_qs(url_having_count.query).get('skip'):
                count = int(parse_qs(url_having_count.query)['skip'][0])
            else:
                count = int(fullmatch(r'item(?P<num>\d+)', url_having_count.fragment).groupdict()['num']) - 1  # type: ignore
            assert count > 0

            date_ = item['date'][0]
            title = item['title']
            count_noun = 'entries' if count > 1 else 'entry'
            title = f'{category} ({title}): {count} new {count_noun} for {date_}'
            link = f'{config.HTML_URL_TEMPLATE_RECENT.format(category=category, count=count)}#{parse_date(date_).date()}'
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

import datetime
import logging.config
import os
from pathlib import Path


def configure_logging() -> None:
    logging.config.dictConfig(LOGGING)
    log = logging.getLogger(__name__)
    log.debug('Logging is configured.')


CACHE_TTL = datetime.timedelta(hours=1, minutes=-4).total_seconds()
CATEGORIES = 'stat.ML', 'cs.LG', 'cs.NE', 'cs.AI', 'cs.CL', 'cs.CV', 'cs.IR', 'eess.IV'
FEED_DESCRIPTION = 'As a disclaimer, this is an unofficial feed and has no affiliation with arXiv.'
FEED_TITLE = 'arXiv ML/AI daily meta updates (unaffiliated)'
HTML_HEXT = """
<div id="dlpage">
    <h1 @text:title/>
    <ul>
        <li>
            <a href:link @text:date/>
        </li>
    </ul>
</div>
"""
HTML_URL_TEMPLATE_RECENT = 'https://arxiv.org/list/{category}/recent?show={count}'
HTML_URL_TEMPLATE_MINIMAL = 'https://arxiv.org/list/{category}/pastweek?show=5'
HTTP_TIMEOUT = 30
MAX_CONNECTIONS = 4
ON_SERVERLESS = bool(os.getenv('GCLOUD_PROJECT'))
DEBUG_ASYNCIO = not ON_SERVERLESS
PACKAGE_NAME = Path(__file__).parent.stem
REPO_URL = 'https://github.com/ml-feeds/arxiv-daily-ml-feed'

LOGGING = {  # Ref: https://docs.python.org/3/howto/logging.html#configuring-logging
    'version': 1,
    'formatters': {
        'detailed': {
            'format': '[%(relativeCreated)i] %(name)s:%(lineno)d:%(funcName)s:%(levelname)s: %(message)s',
        },
        'serverless': {
            'format': '%(thread)x:%(name)s:%(lineno)d:%(funcName)s:%(levelname)s: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'serverless' if ON_SERVERLESS else 'detailed',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        PACKAGE_NAME: {
            'level': 'INFO' if ON_SERVERLESS else 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'asyncio': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        '': {
            'level': 'DEBUG',
            'handlers': ['console'],
         },
    },
}

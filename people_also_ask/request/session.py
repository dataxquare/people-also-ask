import os
import logging
import requests
import traceback
import people_also_ask.config as config

from people_also_ask.tools import retryable
from itertools import cycle
from typing import Optional
from people_also_ask.tools import CallingSemaphore
from people_also_ask.exceptions import RequestError
from requests import Session

NB_TIMES_RETRY = os.environ.get(
    "RELATED_QUESTION_NB_TIMES_RETRY", 3
)
NB_REQUESTS_LIMIT = os.environ.get(
    "RELATED_QUESTION_NB_REQUESTS_LIMIT", 25
)
NB_REQUESTS_DURATION_LIMIT = os.environ.get(
    "RELATED_QUESTION_NB_REQUESTS_DURATION_LIMIT", 60  # seconds
)
semaphore = CallingSemaphore(
    NB_REQUESTS_LIMIT, NB_REQUESTS_DURATION_LIMIT
)
HEADERS = {
    'User-Agent': config.SCRAPPER_USER_AGENT
}


logger = logging.getLogger('app')


class ProxyGeneator:

    def __init__(self, proxies: Optional[tuple]):
        self.proxies = proxies

    @property
    def iter_proxy(self):
        if not self.proxies:
            raise ValueError("No proxy found")
        if getattr(self, "_iter_proxy", None) is None:
            self._iter_proxy = cycle(self.proxies)
        return self._iter_proxy

    def get(self) -> dict:
        if not self.proxies:
            return {}
        proxy = next(self.iter_proxy)
        return {
            "http": proxy
        }


def _load_proxies() -> Optional[tuple]:
    filepath = os.getenv("PAA_PROXY_FILE")
    if filepath:
        with open(filepath, "w") as fd:
            proxies = [e.strip() for e in fd.read().splitlines() if e.strip()]
    else:
        proxies = None
    return proxies


def set_proxies(proxies: Optional[tuple]) -> ProxyGeneator:
    global PROXY_GENERATORS
    PROXY_GENERATORS = ProxyGeneator(proxies=proxies)


set_proxies(proxies=config.SCRAPPER_HTTP_SERP_PROXY_AGENTS)


@retryable(NB_TIMES_RETRY)
def get(url: str, params) -> requests.Response:
    proxies = PROXY_GENERATORS.get()
    with Session() as SESSION:
        try:
            with semaphore:
                response = SESSION.get(
                    url,
                    params=params,
                    headers=HEADERS,
                    proxies=proxies,
                )
        except Exception:
            raise RequestError(
                url, params, proxies, traceback.format_exc()
            )
        if response.status_code != 200:
            raise RequestError(
                url, params, proxies, response.text
            )
        return response

import grequests
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from typing import Generator


class DataFetcher:
    PEOPLE_URL = 'https://swapi.dev/api/people/'
    PLANETS_URL = 'https://swapi.dev/api/planets/'

    def __init__(self, url: str):
        retry_strategy = Retry(
            total=5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=['GET'],
        )
        self._session = Session()
        self._session.mount(
            prefix='https://',
            adapter=HTTPAdapter(max_retries=retry_strategy)
        )
        self._url = url
        self._is_done = False

    def async_fetch(self, limit: int = 10) -> Generator[Generator[dict, None, None], None, None]:
        offset = 1
        while not self._is_done:
            yield (resp for resp in self._filter_until_done(self._fetch_batch(offset, limit)))
            offset += limit

    def _filter_until_done(self, responses: Generator[dict, None, None]) -> Generator[dict, None, None]:
        for resp in responses:
            results = resp.get('results')
            if results is not None:
                yield results
            if resp.get('next') is None:
                self._is_done = True

    def _fetch_batch(self, offset: int, limit: int) -> Generator[dict, None, None]:
        urls = [self._prepare_url(offset) for offset in range(offset, offset + limit)]
        reqs = (grequests.get(url, session=self._session) for url in urls)
        for resp in grequests.map(reqs, stream=False):
            yield resp.json()

    def _prepare_url(self, page_no: int = 1) -> str:
        return f'{self._url}?page={page_no}'

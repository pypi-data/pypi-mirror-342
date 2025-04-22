import itertools
import random

import requests
from requests import compat


class Endpoints:

    def __init__(self, endpoints):
        random.shuffle(endpoints)
        self._endpoints = itertools.cycle(endpoints)
        self._endpoint = next(self._endpoints)

    def shift(self):
        self._endpoint = next(self._endpoints)

    def make_url(self, path) -> str:
        return compat.urljoin(self._endpoint, path)


class HttpClient(requests.Session):

    def __init__(self, base, timeout=1, auth=None, verify=True):
        if isinstance(base, str):
            base = Endpoints([base])
        self._base = base
        self._timeout = timeout
        super().__init__()
        self.auth = auth
        self.verify = verify

    def prepare_request(self, request: requests.Request,
                        ) -> requests.PreparedRequest:
        url = request.url.lower()
        for prefix in self.adapters.keys():
            if url.startswith(prefix.lower()):
                break
        else:
            request.url = self._base.make_url(request.url)

        return super().prepare_request(request)

    def send(self, request, timeout=None, **kwargs):
        if timeout is None:
            timeout = self._timeout

        try:
            return super().send(request, timeout=timeout, **kwargs)
        except Exception:
            self._base.shift()
            raise

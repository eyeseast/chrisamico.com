"""
Parse a URL and return OG values
"""
import re
import httpx
from bs4 import BeautifulSoup

OG_RE = re.compile(r"^og:")


class OpenGraph:
    """
    OpenGraph metadata for a given URL

    >>> og = OpenGraph.fetch('http://www.imdb.com/title/tt0117500/')
    >>> og['title']
    'The Rock (1996)'
    >>> og['type']
    'video.movie'
    >>> og['url']
    'http://www.imdb.com/title/tt0117500/'
    >>> og['image']
    'https://m.media-amazon.com/images/M/MV5BZDJjOTE0N2EtMmRlZS00NzU0LWE0ZWQtM2Q3MWMxNjcwZjBhXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_UY1200_CR90,0,630,1200_AL_.jpg'
    """

    def __init__(self, html, **defaults):

        self._html = html
        self._og = defaults
        self.parse()

    def __getitem__(self, key):
        return self._og[key]

    def __setitem__(self, key, value):
        self._og[key] = value

    def __repr__(self):
        return repr(self._og)

    def get(self, key, default=None):
        return self._og.get(key, default)

    def keys(self):
        return self._og.keys()

    def values(self):
        return self._og.values()

    def items(self):
        return self._og.items()

    def setdefault(self, key, default):
        return self._og.setdefault(key, default)

    def pop(self, key):
        return self._og.pop(key)

    @classmethod
    def fetch(Cls, url, *, client=None, **defaults):
        """
        Fetch and parse html from a url
        """
        if client is None:
            client = httpx.Client()

        r = client.get(url)
        return Cls(r.content, **defaults)

    def parse(self):
        "Extract og values from html"
        soup = BeautifulSoup(self._html, "html.parser")
        metas = soup.find_all("meta", property=OG_RE)

        for meta in metas:
            key = meta["property"].lstrip("og:")
            self._og[key] = meta.get("content")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
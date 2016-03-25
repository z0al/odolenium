from urllib.parse import urlparse
import sys

def parse_url(url):
    """
    Parse URL from string and returns None if the given url is not valid.
    """
    r = urlparse(url)
    if not r.scheme or not r.netloc:
        return None
    return r

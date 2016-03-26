#! python3
# -*- coding: utf-8 -*-
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

def urlgen(url, path=""):
    """
    Generate URL.
    """
    base = "://".join([url.scheme, url.netloc])
    return u"{base:s}/{path:s}".format(
        base=base,
        path=path.lstrip("/"),
    )
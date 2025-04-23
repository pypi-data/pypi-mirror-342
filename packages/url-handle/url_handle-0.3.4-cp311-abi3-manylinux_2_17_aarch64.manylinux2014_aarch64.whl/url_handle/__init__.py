import regex


class UrlEnv:
    def __init__(self, block_regex: regex.Pattern, tld_regex: regex.Pattern, sub_domain_regex: regex.Pattern,
                 proxy_tld_domain: str,
                 server_url: str, server_tld_url: str,
                 sub_domain: str = '', base_url: str = ''):
        self.block_regex = block_regex
        self.tld_regex = tld_regex
        self.sub_domain_regex = sub_domain_regex
        self.server_url = server_url
        self.server_tld_url = server_tld_url
        self.proxy_tld_domain = proxy_tld_domain
        self.sub_domain = sub_domain
        self.base_url = base_url


class UrlHandleWrapper():
    def __init__(self, config: dict):
        pass

    def btoa(self, data: str) -> str:
        pass

    def mitm_url(self, env: UrlEnv, url: str, subdomain: str = None) -> str:
        pass

    def reverse_url(self, env: UrlEnv, url: str, base: str = None) -> str:
        pass

from .url_handle import *
__doc__ = url_handle.__doc__
if hasattr(url_handle, "__all__"):
    __all__ = url_handle.__all__

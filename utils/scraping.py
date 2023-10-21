# -*- coding:utf-8 -*-
# builtins
import functools

# site-packages
import requests
from fake_useragent import UserAgent
from requests.structures import CaseInsensitiveDict

# my-packages
from utils.decorator import param_decorator


__all__ = ['fake_useragent_decorator', 'request_as_get']

_ua = UserAgent()


@param_decorator
def fake_useragent_decorator(f, browser='random'):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        k_headers = 'headers'
        k_user_agent = 'User-Agent'

        # get headers as a case-insensitive dictionary
        headers = CaseInsensitiveDict(kwargs.get(k_headers))

        # set 'User-Agent'
        headers[k_user_agent] = _ua[browser]

        # update
        kwargs.update({k_headers: headers})

        return f(*args, **kwargs)

    return wrapper

@fake_useragent_decorator()
@functools.wraps(requests.get)
def request_as_get(url, headers=None, params=None, proxies=None, **kwargs):

    if proxies:
        kwargs['proxies'] = proxies

    return requests.get(url=url, headers=headers, params=params, **kwargs)


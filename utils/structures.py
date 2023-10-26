# -*- coding:utf-8 -*-
# builtins

# site-packages
from requests.structures import CaseInsensitiveDict as CaseInsensitiveDictRaw

# my-packages


__all__ = ['CaseInsensitiveDict']

class CaseInsensitiveDict(CaseInsensitiveDictRaw):
    def as_dict(self):
        return dict(self)



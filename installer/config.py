# -*- coding:utf-8 -*-
# builtins
from collections import namedtuple

# site-packages

# my-packages


__all__ = ['TorInstallerConfigKey']


TorInstallerConfigKey = namedtuple('TorInstallerConfigKey', ['URLS', 'TARGETS', 'TARGET'])(
    'urls', 'targets', 'target'
)

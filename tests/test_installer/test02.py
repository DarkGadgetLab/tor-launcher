# -*- coding:utf-8 -*-
# builtins
import logging

# site-packages

# my-packages
from installer import TorInstaller
from installer.cache import TorCache

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    tor_cache = TorCache(filename='sample.json')
    tor_cache.dirpath = 'sample'
    tor_installer = TorInstaller(cache=tor_cache)
    #tor_installer.search()
    tor_installer.install(download_dir='download', extract_dir='extract')




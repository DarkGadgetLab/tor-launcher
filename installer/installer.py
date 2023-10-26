# -*- coding:utf-8 -*-
# builtins
import os
import sys
import re
import platform
import threading
import pathlib
from logging import getLogger
from shutil import unpack_archive

# site-packages
from bs4 import BeautifulSoup

# my-packages
from utils import scraping
from installer.config import TorInstallerConfigKey
from installer.cache import TorCache


__all__ = ['TorInstaller']

logger = getLogger(__name__)

class TorInstaller:
    _URL = 'https://www.torproject.org/download/tor/'
    _EXT = '.tar.gz'

    def __init__(self, cache=TorCache(filename='install.json')):
        self.parser = 'html.parser'
        self.__cache = cache
        self.__target = None


    @property
    def url(self):
        return TorInstaller._URL

    @property
    def ext(self):
        return TorInstaller._EXT

    @property
    def cache(self):
        return self.__cache

    def search(self):
        """search"""
        return self.get_target()


    def install(self, download_dir, extract_dir):
        """install"""
        return self.decompress(filepath=self.download(dist_dir=download_dir), extract_dir=extract_dir)


    def download(self, dist_dir):
        """download"""
        logger.info('[*] download starts')
        dist_dir = os.path.abspath(dist_dir)
        target = self.get_target()

        logger.info('[+] download -> %r' % target)
        res = scraping.request_as_get(url=target)
        if not res.ok:
            logger.warning('[!!] download failure - %r' % target)
            return ''

        if not os.path.isdir(dist_dir):
            logger.info('[+] create a directory -> %r' % dist_dir)
            os.makedirs(dist_dir, exist_ok=True)

        filepath = os.path.abspath(os.path.join(dist_dir, os.path.basename(target)))
        with open(filepath, mode='wb') as fd:
            fd.write(res.content)

        logger.info('[*] download successful !!')
        return filepath


    def decompress(self, filepath, extract_dir=None):
        """decompress"""
        logger.info('[*] decompress starts')
        filepath = os.path.abspath(filepath)

        extract_dir = (os.path.abspath(extract_dir)
                       if extract_dir else os.path.dirname(extract_dir))


        logger.info('[+] decompress -> %r' % filepath)
        unpack_archive(filename=filepath, extract_dir=extract_dir)

        f = os.path.basename(filepath).replace(self.ext, '')
        f = pathlib.Path(os.path.normpath(os.path.join(extract_dir, f)))
        f.touch()
        logger.debug('[+] create a version file -> %r' % f.absolute())
        logger.info('[*] decompress successful !!')

        return extract_dir


    def __search(self):
        res = scraping.request_as_get(url=self.url)
        if not res.ok:
            return {}

        targets = [elem.get('href') for elem in BeautifulSoup(res.content, self.parser).select('a[href].downloadLink')]
        return {TorInstallerConfigKey.URLS: targets}


    def __generate_download_pattern(self):
        system = platform.system().lower()

        bit32 = 'i686'
        bit64 = 'x86_64'

        bits = bit64 if sys.maxsize > 2**32 else bit32

        fmt = '-{os}-{bits}.*?{ext}'
        if system == 'windows':
            pattern = fmt.format(os=system, bits=bits, ext=self.ext)

        else:
            raise RuntimeError("[!!] Platform not supported - %r" % system)


        return re.compile(pattern)


    def __get_targets(self):
        pattern = self.__generate_download_pattern()
        if not os.path.isfile(self.cache.filepath):
            self.cache.touch()
            self.cache.write(self.__search())

        self.cache.load()

        selected_targets = [target
                            for target in self.cache.data.get(TorInstallerConfigKey.URLS)
                            if pattern.search(str(target).lower())]

        self.cache.write({TorInstallerConfigKey.TARGETS: selected_targets}, top=True)

        return selected_targets


    def get_target(self):
        with self.get_target.lock:
            self.cache.load()

            target = self.cache.data.get(TorInstallerConfigKey.TARGET)
            if target:
                self.__target = target

            else:
                self.__target = self.__get_targets()[0]

            self.cache.write({TorInstallerConfigKey.TARGET: self.__target}, top=True)

            return self.__target

    get_target.lock = threading.Lock()



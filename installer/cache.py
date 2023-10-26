# -*- coding:utf-8 -*-
# builtins
import json
import os
import threading
import functools

# site-packages

# my-packages
from utils.structures import CaseInsensitiveDict


__all__ = ['TorCache']


class TorCache:
    def __init__(self, filename):
        self.__data = CaseInsensitiveDict()

        self.encoding = 'utf-8'
        self.indent   = 2

        self.__dirpath  = 'cache'
        self.__filename = filename

    @property
    def data(self):
        return self.__data

    @property
    def dirpath(self):
        return self.__dirpath

    @dirpath.setter
    def dirpath(self, dirpath):
        self.__dirpath = os.path.abspath(dirpath)

    @property
    def filepath(self):
        return os.path.join(self.dirpath, self.__filename)


    @staticmethod
    def _threading_lock_decorator(f):
        lock = threading.Lock()
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            with lock:
                return f(self, *args, **kwargs)
        return wrapper


    @_threading_lock_decorator
    def touch(self):
        os.makedirs(self.dirpath, exist_ok=True)
        if not os.path.isfile(self.filepath):
            with open(self.filepath, mode='wt', encoding=self.encoding) as fd:
                fd.write('{}')
        return self.filepath



    @_threading_lock_decorator
    def load(self):
        if not os.path.isfile(self.filepath):
            #raise FileNotFoundError("[!!] the file not found - %r" % self.filepath)
            return

        with open(self.filepath, mode='rt', encoding=self.encoding) as fd:
            self.data.clear()
            self.data.update(json.load(fd))


    @_threading_lock_decorator
    def write(self, obj, top=False):
        with open(self.filepath, mode='rt', encoding=self.encoding) as fd:
            data = json.load(fd)

        if top:
            data, obj = obj, data

        data.update(obj)

        with open(self.filepath, mode='wt', encoding=self.encoding) as fd:
            json.dump(data, fd, indent=self.indent)




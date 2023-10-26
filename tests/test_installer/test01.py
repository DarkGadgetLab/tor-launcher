# -*- coding:utf-8 -*-
# builtins
import logging

# site-packages

# my-packages
from installer import TorInstaller

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    tor_installer = TorInstaller()
    tor_installer.install(download_dir='download', extract_dir='extract')




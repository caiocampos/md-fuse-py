"""
Programa para mesclar arquivos de texto
"""

from fuse import process

CONF_FILE = 'md.conf.json'

process.process(CONF_FILE)

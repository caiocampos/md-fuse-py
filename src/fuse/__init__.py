"""
Programa em python para mesclar arquivos de texto
"""

from .process import process

CONF_FILE = "md.conf.json"


def main() -> int:
    process(CONF_FILE)
    return 0

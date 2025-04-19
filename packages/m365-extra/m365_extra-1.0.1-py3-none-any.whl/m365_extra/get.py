"""
Execute a raw GET request on the API.
"""
import os
from argparse import ArgumentParser

from . import request, M365Client


def add_arguments(parser: ArgumentParser):
    parser.add_argument('endpoint')
    parser.add_argument('--delay', action='store_true', help="wait for all data before creating CSV headers")
    parser.add_argument('-o', '--out', help="output file (CSV if the expected result is tabular, JSON otherwise)")
    

def handle(m365: M365Client, endpoint: str, *, delay = False, out: str|os.PathLike|None = None):
    request.handle(m365, endpoint, 'GET', delay=delay, out=out)

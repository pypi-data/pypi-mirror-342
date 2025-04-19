"""
Execute a raw request on the API.
"""
import os
from argparse import ArgumentParser

from zut import dump_object, tabular_dumper, is_tabular_path

from . import M365Client, settings


def add_arguments(parser: ArgumentParser):
    parser.add_argument('endpoint')
    parser.add_argument('method', nargs='?', default='GET')
    parser.add_argument('data', nargs='?')
    parser.add_argument('--delay', action='store_true', help="wait for all data before creating CSV headers")
    parser.add_argument('-o', '--out', help="output file (CSV if the expected result is tabular, JSON otherwise)")
    

def handle(m365: M365Client, endpoint: str, method: str = 'GET', data: str|dict|None = None, *, delay = False, out: str|os.PathLike|None = None):
    result = m365.raw(endpoint, method=method, data=data)

    if out and not str(out).endswith('.json') and (result.keys() == {'@odata.context', 'value'} or result.keys() == {'@odata.context', 'value', '@odata.nextLink'} or is_tabular_path(out)):
        # tabular output    
        with tabular_dumper(out, dir=settings.DATA_DIR, delay=delay) as dumper:
            for result_data in result['value']:
                dumper.dump(result_data)

            if url := result.get('@odata.nextLink'):
                for result_data in m365.iter(url):
                    dumper.dump(result_data)
    
    else:
        # output is not tabular
        dump_object(result, out, dir=settings.DATA_DIR)

"""
Export list of sites (or a site's details if `site_id` argument is given).
"""
import os
import sys
from argparse import ArgumentParser
from typing import TextIO
from urllib.parse import quote_plus

from zut import dump_object, tabular_dumper

from . import M365Client, settings


def add_arguments(parser: ArgumentParser):
    parser.add_argument('site_id', nargs='?', help="export details of this site only")
    parser.add_argument('-o', '--out', help="output file (CSV, or JSON if `site_id` argument is given)")
    

def handle(m365: M365Client, site_id: str|None = None, *, out: str|os.PathLike|None = None):
    if site_id:
        if out == '.':
            out = '{title}.json'
        dump_site(m365, site_id, out=out)

    else:
        if not out:
            out = '{title}.csv'
        dump_sites(m365, out=out)


def dump_site(m365: M365Client, id: str, *, out: str|os.PathLike|None = '{title}.json', title: str|None = 'site-{id}'):
    data = m365.get(f'/sites/{quote_plus(id)}')
    
    if isinstance(title, str):
        title = title.format(id=data['id'])

    dump_object(data, out, title=title, dir=settings.DATA_DIR)


def dump_sites(m365: M365Client, *, out: str|os.PathLike = '{title}.csv', title: str|None = 'site'):
    for _ in iter_sites(m365, out=out or sys.stdout, title=title):
        pass


def iter_sites(m365: M365Client, *, out: str|os.PathLike|TextIO|None = None, title: str|None = 'site'):
    if out:
        dumper = tabular_dumper(out, headers=['id', 'webUrl', 'displayName', '*'], optional=['name', 'displayName'], title=title, dir=settings.DATA_DIR)
        dumper.__enter__()
    else:
        dumper = None

    try:
        for data in m365.iter('/sites'):
            if dumper:
                dumper.dump(data)
            
            yield data
    finally:
        if dumper:
            dumper.__exit__()

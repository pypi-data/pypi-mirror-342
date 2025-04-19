"""
Export list of groups (or a group's details if `group_id` argument is given).
"""
import os
import sys
from argparse import ArgumentParser
from typing import TextIO
from urllib.parse import quote_plus
from uuid import UUID

from zut import dump_object, tabular_dumper

from . import M365Client, settings


def add_arguments(parser: ArgumentParser):
    parser.add_argument('group_id', nargs='?', help="export details of this group ID only")
    parser.add_argument('-o', '--out', help="output file (CSV, or JSON if `group_id` argument is given)")
    

def handle(m365: M365Client, group_id: str|UUID|None = None, *, out: str|os.PathLike|None = None):
    if group_id:
        if out == '.':
            out = '{title}.json'
        dump_group(m365, group_id, out=out)
    
    else:
        if not out:
            out = '{title}.csv'
        dump_groups(m365, out=out)


def dump_group(m365: M365Client, id: str|UUID, *, out: str|os.PathLike|None = '{title}.json', title: str|None = 'group-{id}'):
    if isinstance(id, UUID):
        id = str(id)
    elif not isinstance(id, str):
        raise TypeError(f"Invalid type for group id: {type(id).__name__}")
    
    data = m365.get(f'/groups/{quote_plus(id)}')
    
    if isinstance(title, str):
        title = title.format(id=data['id'])

    dump_object(data, out, title=title, dir=settings.DATA_DIR)


def dump_groups(m365: M365Client, *, out: str|os.PathLike = '{title}.csv', title: str|None = 'group'):
    for _ in iter_groups(m365, out=out or sys.stdout, title=title):
        pass


def iter_groups(m365: M365Client, *, out: str|os.PathLike|TextIO|None = None, title: str|None = 'group'):    
    if out:
        # NOTE: delay=True so that extneion headers (e.g. extension_0b7a35b5aa1e4b1cbe45e6b988bbd006_mscloud) are added without a warning
        dumper = tabular_dumper(out, headers=["id", "displayName", "*"], delay=True, title=title, dir=settings.DATA_DIR)
        dumper.__enter__()
    else:
        dumper = None

    try:
        for data in m365.iter('/groups'):
            if dumper:
                dumper.dump(data)

            yield data
    finally:
        if dumper:
            dumper.__exit__()

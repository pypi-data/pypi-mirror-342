"""
Export list of users (or a user's details if `user_key` argument is given).
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
    parser.add_argument('user_key', nargs='?', help="export details of this user only, given as its ID or userPrincipalName (usually the email)")
    parser.add_argument('-o', '--out', help="output file (CSV, or JSON if `user` argument is given)")
    

def handle(m365: M365Client, user_key: str|UUID|None = None, *, out: str|os.PathLike|None = None):
    if user_key:        
        if out == '.':
            out = '{title}.json'
        dump_user(m365, user_key, out=out)
    
    else:
        if not out:
            out = '{title}.csv'        
        dump_users(m365, out=out)


def dump_user(m365: M365Client, key: str|UUID, *, out: str|os.PathLike|None = '{title}.json', title: str|None = 'user-{key}'):
    if isinstance(key, UUID):
        key = str(key)
    elif not isinstance(key, str):
        raise TypeError(f"Invalid type for user key: {type(key).__name__}")
    
    data = m365.get(f'/users/{quote_plus(key)}')
    
    if isinstance(title, str):
        title = title.format(key=data['userPrincipalName'])

    dump_object(data, out, title=title, dir=settings.DATA_DIR)


def dump_users(m365: M365Client, *, out: str|os.PathLike = '{title}.csv', title: str|None = 'user'):
    for _ in iter_users(m365, out=out or sys.stdout, title=title):
        pass


def iter_users(m365: M365Client, *, out: str|os.PathLike|TextIO|None = None, title: str|None = 'user'):
    if out:
        dumper = tabular_dumper(out, headers=["id", "userPrincipalName", "displayName", "givenName", "surname", "mail", "businessPhones", "mobilePhone", "jobTitle", "officeLocation", "preferredLanguage"], title=title, dir=settings.DATA_DIR)
        dumper.__enter__()
    else:
        dumper = None

    try:
        for data in m365.iter('/users'):
            if dumper:
                dumper.dump(data)
            
            yield data
    finally:
        if dumper:
            dumper.__exit__()

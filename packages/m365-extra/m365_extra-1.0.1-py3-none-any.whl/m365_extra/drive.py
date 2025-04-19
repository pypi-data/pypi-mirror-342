"""
Export list of drives (or a drive's details if `drive_id` argument is given).
"""
import logging
import os
import sys
from argparse import ArgumentParser
from datetime import timedelta
from time import time_ns
from typing import Any, TextIO
from urllib.parse import quote_plus
from uuid import UUID

import requests
from zut import dump_object, files, slugify, tabular_dumper

from . import DriveParentType, M365Client, OwnerType, settings

_logger = logging.getLogger(__name__)


def add_arguments(parser: ArgumentParser):
    parser.add_argument('drive_id', nargs='?', help="export details of this drive only")
    parser.add_argument('-o', '--out', help="output file (CSV, or JSON if `drive_id` argument is given)")


def handle(m365: M365Client, drive_id: str|None = None, *, out: str|os.PathLike|None = None):
    if drive_id:        
        if out == '.':
            out = '{title}.json'
        dump_drive(m365, drive_id, out=out)

    else:
        if not out:
            out = '{title}.csv'        
        dump_drives(m365, out=out)


def dump_drive(m365: M365Client, id: str, *, out: str|os.PathLike|None = '{title}.json', title: str|None = 'drive-{id}'):
    data = m365.get(f'/drives/{quote_plus(id)}')
    
    if isinstance(title, str):
        title = title.format(id=data['id'])

    dump_object(data, out, title=title, dir=settings.DATA_DIR)


def dump_drives(m365: M365Client, *, out: str|os.PathLike = '{title}.csv', title: str|None = 'drive', interval: float|int|bool|None = None):
    for _ in iter_drives(m365, out=out, title=title, interval=interval):
        pass


def dump_parent_drives(m365: M365Client, parent_type: DriveParentType, parent_data: str|UUID|dict[str,Any], *, out: str|os.PathLike = '{title}.csv', title: str|None = 'drive-{parent}', interval: float|int|bool|None = None):
    for _ in iter_parent_drives(m365, parent_type, parent_data, out=out or sys.stdout, title=title, interval=interval):
        pass


def iter_drives(m365: M365Client, *, out: str|os.PathLike|None = None, title: str|None = 'drive', interval: float|int|bool|None = None):
    total_count = 0
    t0 = time_ns()

    if out:
        out = files.in_dir(out, dir=settings.DATA_DIR, title=title)
        files.remove(out, missing_ok=True)

        _logger.info(f"Dump drives to {out} …")

    next_t = 0
    interval_auto = False    
    if interval is True or (interval is None and out):
        interval = 5.0
        interval_auto = True
    if interval:
        next_t = t0 + interval * 1E9

    for drive_type in [DriveParentType.USER, DriveParentType.GROUP, DriveParentType.SITE]:
        _logger.info(f"Search {drive_type.name.lower()} drives …")
        type_count = 0
        try:
            for parent_data in m365.iter(f'/{drive_type.name.lower()}s?$select=id,displayName'):
                try:
                    for drive_data in iter_parent_drives(m365, drive_type, parent_data, out=out, append=True, title=False, interval=False):
                        type_count += 1
                        total_count += 1

                        if interval:
                            t = time_ns()
                            if t >= next_t:
                                _logger.info(f"{total_count:,} drives found …")
                                if interval_auto:
                                    if interval < 60.0:
                                        interval = interval + 5.0
                                next_t = t + interval * 1E9

                        yield drive_data
                except:
                    _logger.exception("Failure while exporting drives for %s %s: %s", drive_type.name.lower(), parent_data.get('id'), parent_data.get('displayName'))
        except:
            _logger.exception("Failure while reading %ss", drive_type.name.lower())

        _logger.info(f"{drive_type.name.lower().capitalize()} drives: {type_count:,} found")

    if out:
        _logger.info(f"{total_count:,} drives dumped to {out} in {timedelta(seconds=int((time_ns() - t0)/1E9))}")
    elif interval:
        _logger.info(f"Total: {total_count:,} drives found in {timedelta(seconds=int((time_ns() - t0)/1E9))}")


def iter_parent_drives(m365: M365Client, parent_type: DriveParentType, parent_data: str|UUID|dict[str,Any], *, out: str|os.PathLike|TextIO|None = None, append = False, title: str|bool|None = 'drive-{parent}', interval: float|int|bool|None = None):
    if isinstance(parent_data, dict):
        parent_id = parent_data['id']
        parent_display_name = parent_data.get('displayName')
    elif isinstance(parent_data, UUID):
        parent_id = str(parent_data)
        parent_display_name = None
    elif isinstance(parent_data, str):
        parent_id = parent_data
        parent_display_name = None

    if out:
        if isinstance(title, str):
            title = title.format(parent=f"{parent_type.name.lower()}-{parent_id}")
        dumper = tabular_dumper(out, append=append, title=title, interval=interval, dir=settings.DATA_DIR)
        dumper.__enter__()
    else:
        dumper = None

    endpoint = f"/{parent_type.name.lower()}s/{quote_plus(parent_id)}/drives"

    try:
        for data in m365.iter(endpoint):
            if dumper:
                owner_id, owner_type, owner_email, owner_display_name = _get_user_or_group_details(data['owner'])
                created_by_id, created_by_type, created_by_email, created_by_display_name = _get_user_or_group_details(data['createdBy'])

                dumper.dump({
                    'id': data['id'],
                    'webUrl': data['webUrl'],
                    'name': data['name'],
                    'description': data['description'],
                    'driveType': data['driveType'],
                    'owner_id': owner_id,
                    'owner_type': owner_type,
                    'owner_email': owner_email,
                    'owner_displayName': owner_display_name,
                    'createdBy_id': created_by_id,
                    'createdBy_type': created_by_type,
                    'createdBy_email': created_by_email,
                    'createdBy_displayName': created_by_display_name,
                    'createdDateTime': data['createdDateTime'],
                    'lastModifiedDateTime': data['lastModifiedDateTime'],
                    'quota_state': data['quota']['state'],
                    'quota_total': data['quota']['total'] / 1024**3,
                    'quota_used': data['quota']['used'] / 1024**3,
                    'quota_deleted': data['quota']['deleted'] / 1024**3,
                    'quota_remaining': data['quota']['remaining'] / 1024**3,
                    'parent_id': parent_id,
                    'parent_type': parent_type,
                    'parent_displayName': parent_display_name,
                })

            yield data
    except m365.Error as err:
        if err.code == 404:
            pass # parent has no drives (ResourceNotFound (code 404): User's mysite not found)
        else:
            raise
    finally:
        if dumper:
            dumper.__exit__()


def _get_user_or_group_details(data: dict) -> tuple[str|None, OwnerType, str|None, str]:
    if sub := data.get('user'):
        owner_type = OwnerType.USER
    elif sub := data.get('group'):
        owner_type = OwnerType.GROUP
    else:
        raise ValueError(f"Missing user or group in {data}")

    #NOTE: id and email are not present for "system account" user and others (deleted?)
    return sub.get('id'), owner_type, sub.get('email'), sub['displayName']

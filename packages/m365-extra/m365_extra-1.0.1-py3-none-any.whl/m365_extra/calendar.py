"""
Export list of calendars (or a calendar's details if `calendar_id` argument is given).

See:
- API endpoints:
    - https://learn.microsoft.com/en-us/graph/api/user-list-calendargroups?view=graph-rest-1.0&tabs=http
    - https://learn.microsoft.com/en-us/graph/api/user-list-calendars?view=graph-rest-1.0&tabs=http
- Event type: https://learn.microsoft.com/en-us/graph/api/resources/event?view=graph-rest-1.0

[ROADMAP?] Note: it is not possible to extract group calendar or group calendar events from an application (only delegated permissions are supported - which would require being a member of each group).
See https://learn.microsoft.com/en-us/graph/api/calendar-list-events?view=graph-rest-beta&tabs=http#permissions
"""
import logging
import os
from argparse import ArgumentParser
from datetime import timedelta
from time import time_ns
from urllib.parse import quote_plus
from uuid import UUID

from zut import dump_object, files, is_tabular_path, tabular_dumper

from . import M365Client, OwnerType, settings

_logger = logging.getLogger(__name__)


def add_arguments(parser: ArgumentParser):
    parser.add_argument('user', nargs='?', help="export list of calendar events for this user only (or FROM this user with `--from-user` option), given as its ID or userPrincipalName (usually the email)")
    parser.add_argument('--from-user', action='store_true', help="export list of calendar events for all users starting from the given `user` argument")
    parser.add_argument('-o', '--out', default='{title}.csv', help="output CSV file")
    

def handle(m365: M365Client, user: str|UUID|None = None, *, from_user = False, out: str|os.PathLike = '{title}.csv'):
    if from_user:
        if not user:
            raise ValueError("Argument 'user' is required for option 'from_user'")

    if user and not from_user:
        dump_user_calendars(m365, user, out=out)
    else:
        dump_calendars(m365, from_user=user, out=out)


def dump_calendars(m365: M365Client, *, from_user: str|UUID|None = None, out: str|os.PathLike = '{title}.csv'):
    if isinstance(from_user, UUID):
        from_user = str(from_user)
    
    if from_user:
        started = False
        title = f'calendar-from-{from_user}'
    else:
        started = None
        title = f'calendar'

    out = files.in_dir(out, dir=settings.DATA_DIR, title=title)
    files.remove(out, missing_ok=True)
    
    t0 = time_ns()
    _logger.info(f"Dump calendars to {out} …")
    total_count = 0

    for user_data in m365.iter('/users'):
        if from_user and not started:
            if user_data['userPrincipalName'] == from_user or user_data['id'] == from_user:
                started = True
            else:
                continue

        try:
            _logger.info("Search calendars for user %s …", user_data['userPrincipalName'])
            count = dump_user_calendars(m365, user_data, out=out, title=None, append=True)
            total_count += count
            _logger.info("%s calendars found for user %s", count, user_data['userPrincipalName'])
        except Exception as err:
            _logger.exception("Error while exporting calendars for user %s" % (user_data['userPrincipalName'],))

    _logger.info(f"{total_count:,} calendars exported to {out} in {timedelta(seconds=int((time_ns() - t0)/1E9))}")


def dump_user_calendars(m365: M365Client, user: str|UUID|dict, *, out: str|os.PathLike = '{title}.csv', title: str|None = 'calendar-{user}', append = False):
    if isinstance(user, str):
        try:
            user = UUID(user)
        except ValueError:
            pass # user is not a uuid
    
    owner_id = None
    owner_principal_name = None
    owner_display_name = None
    if isinstance(user, UUID):
        owner_id = user
        user_endpoint = f'/users/{owner_id}'
    elif isinstance(user, str):
        owner_principal_name = user
        user_endpoint = f'/users/{quote_plus(owner_principal_name)}'
    elif isinstance(user, dict):
        owner_id = user['id']
        owner_principal_name = user['userPrincipalName']
        owner_display_name = user['displayName']
        user_endpoint = f'/users/{owner_id}'
    else:
        raise TypeError(f"Invalid type for argument 'user': {type(user).__name__}")
    
    if isinstance(title, str):
        title = title.format(user=owner_principal_name or owner_id)

    endpoint = f'{user_endpoint}/calendars'
    if not is_tabular_path(out):
        if out == '.':
            out = '{title}.json'

        data_list = m365.get(endpoint)
        dump_object(data_list, out, title=title, dir=settings.DATA_DIR)
        return len(data_list)
    else:
        with tabular_dumper(out, headers=['id', 'owner_id', 'owner_type', 'owner_email', 'owner_displayName', 'name', 'isDefaultCalendar', 'canEdit'], title=title, append=append, dir=settings.DATA_DIR) as dumper:
            try:
                for data in m365.iter(endpoint):
                    dumper.dump({
                        'id': data['id'],
                        'owner_id': owner_id,
                        'owner_type': OwnerType.USER.value,
                        'owner_email': owner_principal_name,
                        'owner_displayName': owner_display_name,
                        'name': data['name'],
                        'isDefaultCalendar': data['isDefaultCalendar'],
                        'canEdit': data['canEdit'],
                    })
            except m365.MailboxInactiveError:
                _logger.debug("Mailbox inactive for user %s", owner_principal_name or owner_id)
                return 0

        return dumper.count

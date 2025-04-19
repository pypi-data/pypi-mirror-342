"""
Export list of calendar events (or a calendar event's details if `event_id` argument is given).

See:
- API endpoints: https://learn.microsoft.com/en-us/graph/api/calendar-list-events?view=graph-rest-1.0&tabs=http
- Event type: https://learn.microsoft.com/en-us/graph/api/resources/event?view=graph-rest-1.0

Note: it is not possible to extract group calendar or group calendar events from an application (only delegated permissions are supported - which would require being a member of each group).
See https://learn.microsoft.com/en-us/graph/api/calendar-list-events?view=graph-rest-beta&tabs=http#permissions
"""
from datetime import timedelta
import logging
import os
from argparse import ArgumentParser
from time import time_ns
from urllib.parse import quote_plus
from uuid import UUID

from zut import dump_object, files, tabular_dumper

from . import M365Client, settings

_logger = logging.getLogger(__name__)


def add_arguments(parser: ArgumentParser):
    parser.add_argument('user', nargs='?', help="export list of calendar events for this user only (or FROM this user with `--from-user` option), given as its ID or userPrincipalName (usually the email)")
    parser.add_argument('event_id', nargs='?', help="export details of this calendar event only")
    parser.add_argument('--from-user', action='store_true', help="export list of calendar events for all users starting from the given `user` argument")
    parser.add_argument('-o', '--out', help="output file (CSV, or JSON if `event_id` argument is given)")
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--calendar', help="retrict to the given calendar only")
    group.add_argument('--all-calendars', action='store_const', dest='calendar', const='all', help="export events for all calendars of the user (by default, only the default calendar is exported)")
    

def handle(m365: M365Client, user: str|UUID|None = None, event_id: str|None = None, *, calendar: str|None = None, from_user = False, out: str|os.PathLike|None = None):
    if not user:
        if event_id:            
            raise ValueError("Argument 'user' is required for 'event_id'")
        if from_user:
                raise ValueError("Argument 'user' is required for option 'from_user'")
        if calendar and calendar != 'all':
            raise ValueError("Argument 'user' is required for option 'calendar'")
    
    if event_id:
        if out == '.':
            out = '{title}.json'
        user_endpoint = f'/users/{str(user) if isinstance(user, UUID) else quote_plus(user)}' # type: ignore
        data = m365.get(f'{user_endpoint}/calendar/events/{quote_plus(event_id)}')
        dump_object(data, out, title=f"event-{data['id']}" if out else None, dir=settings.DATA_DIR)
    else:
        if not out:
            out = '{title}.csv'
            
        if user and not from_user:
            export_user_event_list(m365, user, calendar=calendar, out=out)
        else:
            export_event_list(m365, all_calendars=calendar == 'all', from_user=user, out=out)


def export_event_list(m365: M365Client, *, all_calendars = False, from_user: str|UUID|None = None, out: str|os.PathLike = '{title}.csv'):
    if isinstance(from_user, UUID):
        from_user = str(from_user)
    
    if from_user:
        started = False
        title = f'event-from-{from_user}'
    else:
        started = None
        title = f'event'

    out = files.in_dir(out, dir=settings.DATA_DIR, title=title)
    files.remove(out, missing_ok=True)
    
    t0 = time_ns()
    _logger.info(f"Dump events to {out} …")
    total_count = 0

    for user_data in m365.iter('/users'):
        if from_user and not started:
            if user_data['userPrincipalName'] == from_user or user_data['id'] == from_user:
                started = True
            else:
                continue

        try:
            _logger.info("Search events for user %s …", user_data['userPrincipalName'])
            count = export_user_event_list(m365, user_data, calendar='all' if all_calendars else None, out=out, title=None, append=True)
            total_count += 0
            _logger.info("%s events found for user %s", count, user_data['userPrincipalName'])
        except Exception as err:
            _logger.exception("Error while exporting events for user %s" % (user_data['userPrincipalName'],))

    _logger.info(f"{total_count:,} events exported to {out} in {timedelta(seconds=int((time_ns() - t0)/1E9))}")


def export_user_event_list(m365: M365Client, user: str|UUID|dict, *, calendar: str|None = None, out: str|os.PathLike = '{title}.csv', title: str|None = 'event-{user}', append = False):
    if isinstance(user, str):
        try:
            user = UUID(user)
        except ValueError:
            pass # user is not a uuid
    
    owner_id = None
    owner_name = None
    if isinstance(user, UUID):
        owner_id = user
        user_endpoint = f'/users/{owner_id}'
    elif isinstance(user, str):
        owner_name = user
        user_endpoint = f'/users/{quote_plus(owner_name)}'
    elif isinstance(user, dict):
        owner_id = user['id']
        owner_name = user['userPrincipalName']
        user_endpoint = f'/users/{quote_plus(owner_name)}'
    else:
        raise TypeError(f"Invalid type for argument 'user': {type(user).__name__}")

    if isinstance(title, str):
        if calendar:
            if '{calendar}' in title:
                title = title.format(user=owner_name or owner_id, calendar=calendar)
            else:
                title = title.format(user=f'{owner_name or owner_id}-{calendar}')
        else:
            title = title.format(user=owner_name or owner_id)
            
    calendars_id = []
    default_calendar_id = None
    if calendar and calendar != 'all':
        calendars_id.append(calendar)
    else:
        try:
            for data in m365.iter(f'{user_endpoint}/calendars'):
                if data['isDefaultCalendar']:
                    default_calendar_id = data['id']
                    calendars_id.append(data['id'])
                elif calendar == 'all':
                    calendars_id.append(data['id'])
        except m365.MailboxInactiveError:
            _logger.debug("Mailbox inactive for user %s", owner_id or owner_name)
            return 0
    
    
    with tabular_dumper(out, headers=['id', 'calendarId', 'iCalUId', 'uid', 'ownerId', 'ownerName', 'ownerType', 'isDefaultCalendar', 'subject', 'start', 'end', 'isAllDay', 'recurrencePatternType', 'originalStartTimeZone', 'originalEndTimeZone', 'createdDateTime', 'lastModifiedDateTime'], title=title, append=append, dir=settings.DATA_DIR) as dumper:    
        for calendar_id in calendars_id:
            for data in m365.iter(f'{user_endpoint}/events'):
                dumper.dump({
                    'id': data['id'],
                    'calendarId': calendar_id,
                    'iCalUId': data['iCalUId'],
                    'uid': data['uid'],
                    'ownerId': owner_id,
                    'ownerName': owner_name,
                    'ownerType': OwnerType.USER.value,
                    'isDefaultCalendar': calendar_id == default_calendar_id,
                    'subject': data.get('subject'),
                    'start': m365.parse_datetime(data['start']),
                    'end': m365.parse_datetime(data['end']),
                    'isAllDay': data.get('isAllDay'),
                    'recurrencePatternType': data['recurrence']['pattern']['type'] if data.get('recurrence') else None,
                    'originalStartTimeZone': data.get('originalStartTimeZone'),
                    'originalEndTimeZone': data.get('originalEndTimeZone'),
                    'createdDateTime': m365.parse_datetime(data['createdDateTime']),
                    'lastModifiedDateTime': m365.parse_datetime(data['lastModifiedDateTime']),
                })
    
    return dumper.count

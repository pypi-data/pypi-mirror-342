"""
Upload a file from the local file system to a M365 drive.

See: https://learn.microsoft.com/en-us/graph/api/driveitem-createuploadsession?view=graph-rest-1.0
"""
import json
import logging
from argparse import ArgumentParser
import os
from pathlib import Path
from time import time_ns
from urllib.parse import quote

from requests import HTTPError
from zut import files

from . import M365Client, settings

_logger = logging.getLogger(__name__)


class Command:
    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('drive_id')
        parser.add_argument('folder')
        parser.add_argument('source')
        parser.add_argument('--fragment-size-mib', type=int, default=50)
        parser.add_argument('--session-file', help="A JSON file to use to keep the upload session URL in case of outage.")
        
    def handle(self, m365: M365Client, drive_id: str, folder: str, source: str|Path, *, fragment_size_mib: int = 50, session_file: str|os.PathLike|None = None, **options):
        self.m365 = m365

        try:
            if folder == 'root':
                folder_data = self.m365.get(f"/drives/{drive_id}/root?$select=id,webUrl")
            elif folder.startswith('id:'):
                folder_data = self.m365.get(f"/drives/{drive_id}/items/{folder.removeprefix('id:')}?$select=id,webUrl")
            else:
                folder_data = self.m365.get(f"/drives/{drive_id}/root:/{'/'.join([quote(part) for part in Path(folder).parts])}?$select=id,webUrl")
        except HTTPError as err:
            if err.response.status_code == 404:
                _logger.error("Folder not found: %s", folder)
                return
            else:
                raise

        folder_id = folder_data['id']
        _logger.info("Found folder id %s: %s", folder_id, folder_data['webUrl'])

        if not isinstance(source, Path):
            source = Path(source)

        total_size = source.stat().st_size

        # Fragments must be multiples of 327 680 bytes and must be less than 60 MiB (= 62 914 560, = 192 x 327 680)
        multiple = 327680
        if fragment_size_mib >= 60:
            _logger.error("Fragment must be less than 60 MiB")
            return
        else:
            fragment_size = fragment_size_mib * 1024 * 1024
            fragment_size -= fragment_size % multiple

        # Request or upload session
        file_url = f"{self.m365.base_url}drives/{drive_id}/items/{folder_id}:/{quote(source.name)}"
        session_url = None
        if session_file:
            session_file = files.in_dir(session_file, settings.DATA_DIR)
            if session_file.exists():
                with open(session_file, 'r') as fp:
                    prev = json.load(fp)
                    if prev['file_url'] == file_url:
                        session_url = prev['session_url']

        t0 = time_ns()
        if session_url:
            try:
                _logger.debug(f"Request missing fragments")
                data = self.m365.get(session_url)
                return
            except HTTPError as err:
                _logger.error(f"Failed to request missing fragments: {err.response.status_code} {err.response.reason} - {err.response.text}")
                return
        else:
            try:
                data = self.m365.post(f'{file_url}:/createUploadSession', {
                    "item": {
                        "@microsoft.graph.conflictBehavior": "fail",
                    },
                    "deferCommit": False
                })
            except HTTPError as err:
                _logger.error(f"Failed to create upload session: {err.response.status_code} {err.response.reason} - {err.response.text}")
                return
            
            session_url = data['uploadUrl']
            expiration = data['expirationDateTime']
            _logger.debug(f"Upload session URL: {session_url} - Expiration: {expiration}")

            if session_file:
                session_file.parent.mkdir(parents=True, exist_ok=True) # type: ignore
                with open(session_file, 'w') as fp:
                    json.dump({
                        'file_url': file_url,
                        'session_url': session_url,
                        'expiration': expiration,
                    }, fp, ensure_ascii=False, indent=2)

        t1 = time_ns()
        next_t = t1 + 1E9

        fragment_num = 0
        fragment_start = 0
        fragment_end = -1
        with open(source, 'rb') as fp:
            while fragment := fp.read(fragment_size):
                fragment_num += 1
                fragment_length = len(fragment)
                fragment_end = fragment_start + fragment_length - 1
                fragment_range = f'bytes {fragment_start}-{fragment_end}/{total_size}'

                try:
                    _logger.debug(f"Upload fragment {fragment_num:,} ({fragment_range}): {fragment_length:,} bytes")
                    data = self.m365.put(session_url, headers={
                        'Content-Length': f'{fragment_length}',
                        'Content-Range': f'{fragment_range}',
                    }, data=fragment, no_authorization=True)

                    fragment_start = fragment_end + 1

                    issue = None
                    unreceived_ranges: list[str] = data.pop('nextExpectedRanges', None)
                    if unreceived_ranges:                        
                        expiration = data.pop('expirationDateTime')
                        try:
                            unreceived_ranges.remove(f'{fragment_start}-{total_size-1}')
                        except ValueError:
                            issue = f"missing nextExpectedRange {f'{fragment_start}-{total_size-1}'}"
                        if unreceived_ranges:
                            issue = f"unexpected nextExpectedRanges {f', '.join(unreceived_ranges)}" + (f' - {issue}' if issue else '')
                        _logger.log(logging.WARNING if issue else logging.DEBUG, f"Fragment {fragment_num} - expiration: %s - %s", expiration, issue if issue else 'OK')
                    else: # transfer ended, we now have details about the file
                        _logger.info(f"File uploaded, id: {data['id']}, name: {data['name']}, mimeType: {data['file']['mimeType']}, quickXorHash: {data['file']['hashes']['quickXorHash']}, webUrl: {data['webUrl']}")
                except HTTPError as err:
                    _logger.error(f"Failed to upload fragment {fragment_num} ({fragment_range}): {err.response.status_code} {err.response.reason} - {err.response.text}")
                    return

                t = time_ns()
                if t >= next_t:
                    size = fragment_end + 1
                    seconds = (t - t1) / 1E9
                    _logger.info(f"{size:,} bytes transfered in {seconds:,.1f} seconds ({size/seconds/(1024*1024):,.3f} MiB/sec) …")
                    next_t = t + 1E9

        t = time_ns()
        size = fragment_end + 1
        _logger.info(f"Done: {size:,} bytes transfered in {(t1 - t0) / 1E9:,.1f}+{(t - t1) / 1E9:,.1f} seconds ({size/((t - t0)/1E9)/(1024*1024):,.3f} MiB/sec)")
        if session_file:
            session_file.unlink(missing_ok=True) # type: ignore

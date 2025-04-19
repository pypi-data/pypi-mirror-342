from argparse import ArgumentParser, RawTextHelpFormatter

from zut import (add_commands, add_command, configure_logging, exec_command,
                 get_description_text)

from . import __version__ # type: ignore
from . import M365Client, __doc__, __prog__, user, group, site, calendar, event, drive, upload, get, request


def add_arguments(parser: ArgumentParser):
    subparsers = parser.add_subparsers(title='commands')
    
    add_command(subparsers, user)
    add_command(subparsers, group)
    add_command(subparsers, site)

    add_command(subparsers, calendar)
    add_command(subparsers, event)

    add_command(subparsers, drive)
    add_command(subparsers, upload)
        
    add_command(subparsers, get)
    add_command(subparsers, request) 


def main(args: list[str]|None = None):
    configure_logging()
    
    parser = ArgumentParser(prog=__prog__, description=get_description_text(__doc__), formatter_class=RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=f"{__prog__} {__version__ or '?'}")
    
    add_arguments(parser)
    exec_command(parser, args, additional_args_builders={'m365': M365Client})


if __name__ == '__main__':
    main()

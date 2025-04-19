from argparse import ArgumentParser, RawTextHelpFormatter

from zut import (add_command, configure_logging, exec_command,
                 get_description_text)

from . import __version__  # pyright: ignore[reportAttributeAccessIssue]
from . import __doc__, __prog__, gpg


def add_arguments(parser: ArgumentParser):
    subparsers = parser.add_subparsers(title='commands')    
    add_command(subparsers, gpg)


def main(args: list[str]|None = None):
    configure_logging()
    
    parser = ArgumentParser(prog=__prog__, description=get_description_text(__doc__), formatter_class=RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=f"{__prog__} {__version__ or '?'}")    
    add_arguments(parser)
    exec_command(parser, args)


if __name__ == '__main__':
    main()

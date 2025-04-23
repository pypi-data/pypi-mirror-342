"""
Main command line interface to the pynorare package.
"""
import argparse
import sys
import contextlib

from clldutils.clilib import (
    register_subcommands, get_parser_and_subparsers, ParserError, PathType, add_format)
from clldutils.loglib import Logging

import pylexibench.commands
from pylexibench.repository import Repository


def RepoType(s):
    try:
        return Repository(PathType(type='dir')(s))
    except AssertionError:
        raise ParserError('{} is not a lexibench repository'.format(s))


def main(args=None, catch_all=False, parsed_args=None):
    parser, subparsers = get_parser_and_subparsers('lexibench')
    parser.add_argument(
        '--repos',
        help="Directory where dataset list can be found and results stored.",
        default=None,
        type=RepoType)
    parser.add_argument(
        '--test',
        action='store_true',
        default=False,
        help=argparse.SUPPRESS,
    )
    add_format(parser, default='simple')

    register_subcommands(subparsers, pylexibench.commands)

    args = parsed_args or parser.parse_args(args=args)
    args.repos = args.repos or RepoType('.')
    if not hasattr(args, "main"):  # pragma: no cover
        parser.print_help()
        return 1

    with contextlib.ExitStack() as stack:
        stack.enter_context(Logging(args.log, level=args.log_level))
        try:
            return args.main(args) or 0
        except KeyboardInterrupt:  # pragma: no cover
            return 0
        except ParserError as e:  # pragma: no cover
            print(e)
            return main([args._command, '-h'])
        except Exception as e:  # pragma: no cover
            if catch_all:  # pragma: no cover
                print(e)
                return 1
            raise


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main() or 0)

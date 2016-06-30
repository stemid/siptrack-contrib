#!/usr/bin/env python
# coding: utf-8
#
# Import keys from json by connecting them to a user in siptrack

from __future__ import print_function

try:
    from configparser import RawConfigParser
except ImportError:
    from ConfigParser import RawConfigParser
from json import loads
from argparse import ArgumentParser, FileType
from pprint import pprint as pp
from sys import exit, stderr, stdin

import siptracklib

parser = ArgumentParser(
    description='Export a list of password keys to a user in siptrack',
    epilog='Example: cat keys.json | ./import.py --user stemid'
)

config = RawConfigParser()

parser.add_argument(
    '-v', '--verbose',
    action='count',
    default=False,
    dest='verbose',
    help='Verbose output, use more v\'s to increase level'
)

parser.add_argument(
    '-u', '--user', '--username',
    required=True,
    help='Username of user to export keys from'
)

parser.add_argument(
    '-c', '--configuration', '--config',
    type=FileType('r'),
    help='Configuration with siptrack connection credentials'
)


def main():
    args = parser.parse_args()

    if args.configuration:
        config.readfp(args.configuration)
    else:
        config.read(
            [
                './siptrack.conf',
                './siptrack_local.conf',
                '/etc/siptrack.conf'
            ]
        )

    st = siptracklib.connect(
        config.get('siptrack', 'hostname'),
        config.get('siptrack', 'username'),
        config.get('siptrack', 'password'),
        config.getint('siptrack', 'port'),
        use_ssl=config.getboolean('siptrack', 'ssl')
    )

    st_view = st.view_tree.getChildByName(
        config.get('siptrack', 'base_view'),
        include=['view']
    )

    # Take the first matching user
    user = st.view_tree.user_manager.getUserByName(args.user)[0]

    subkey_json = stdin.read()
    subkey_data = loads(subkey_json)
    pp(subkey_data)


if __name__ == '__main__':
    main()

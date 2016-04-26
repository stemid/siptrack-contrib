#!/usr/bin/env python
# 
# Search objects in Siptrack by attribute value.
# This is the slow approach and does not use the search index. Because we want
# to find any kind of attribute we must recursively search the entire object
# tree.
#
# by Stefan Midjich <swehack [at] gmail [dot] com>

from __future__ import print_function

from sys import exit, stderr
from fnmatch import fnmatch
from argparse import ArgumentParser, FileType
try:
    from configparser import RawConfigParser
except ImportError:
    from ConfigParser import RawConfigParser

import siptracklib

# Object classes defined in Siptrackdlib
object_classes = [
    'D',
    'C',
    'CT',
    'DT',
    'DC',
    'CQ',
    'CNT',
    'TMPL',
    'CFGNETAUTO',
    'VT',
    'V',
    'CA',
    'PERM',
    'DCTMPL',
    'PT',
    'PC',
    'UM',
    'UML',
    'NT',
    'IP6N',
    'IP6NR',
    'IP4N',
    'IP4NR'
]

_classes = {}
for _class in object_classes:
    _classes[_class] = {'class types': []}

_classes['D']['class types'] = ['device', 'device category']

parser = ArgumentParser()
config = RawConfigParser()

def get_category_by_path(st_dt, path, separator=':'):
    st_category = st_dt
    for com in path.split(separator):
        st_category = st_category.getChildByName(com.encode('utf-8'))
        if not st_category:
            break
    else:
        return st_category


def traverse_objects(st_object, depth=1):
    args = parser.parse_args()

    maxdepth = args.max_recursion

    if depth > maxdepth:
        if args.verbose:
            print('Reached max recursive depth, bailing out like a banker',
                  file=stderr
                 )
        return

    if st_object.class_id == args.object_type:
        attribute = st_object.attributes.get(args.attribute_name, '')
        if fnmatch(attribute, args.attribute_value):
            print('{oid}: {name}: {attr} = {val}'.format(
                oid=st_object.oid,
                name=st_object.attributes.get('name', 'UNKNOWN'),
                attr=args.attribute_name,
                val=attribute
            ))

    search_classes = []
    try:
        search_classes = _classes[args.object_type]['class types']
    except KeyError:
        pass

    for child in st_object.listChildren(include=search_classes):
        traverse_objects(child, depth+1)


parser.add_argument(
    '-v', '--verbose',
    action='count',
    default=False,
    dest='verbose',
    help='Verbose output, use more v\'s to increase verbosity'
)

parser.add_argument(
    '-c', '--configuration',
    type=FileType('r'),
    required=True,
    help='Configuration with siptrack connection credentials'
)

parser.add_argument(
    '-d', '--device-path',
    action='store',
    required=True,
    dest='device_path',
    help=('Path to the device category to use as root for the import. '
          'Separate path components with : (semicolon) by default.'
          'Example: -d \'Public Cloud:Devices\'')
)

parser.add_argument(
    '-m', '--max-recursion',
    default=16,
    help='Maximum recursive depth for searching'
)

parser.add_argument(
    '-T', '--object-type',
    choices=object_classes,
    default='D',
    metavar='OBJECT_TYPE',
    help='Object type to search for, use --list-object-types to see list'
)

parser.add_argument(
    '--list-object-types',
    action='store_true',
    help='List available object types'
)

parser.add_argument(
    '-A', '--attribute-name',
    default='name',
    help='Attribute name to search for'
)

parser.add_argument(
    '-V', '--attribute-value',
    required=True,
    help='Attribute value to search for. Takes wildcards like fnmatch'
)

args = parser.parse_args()
config.readfp(args.configuration)

# Only list object class types and exit
if args.list_object_types:
    print(object_classes)
    exit(0)

st = siptracklib.connect(
    config.get('siptrack', 'hostname'),
    config.get('siptrack', 'username'),
    config.get('siptrack', 'password'),
    config.get('siptrack', 'port'),
    use_ssl=config.getboolean('siptrack', 'ssl')
)

# Use the base view defined in the configuration
st_view = st.view_tree.getChildByName(
    config.get('siptrack', 'base_view'),
    include=['view']
)

# Siptrack device tree
st_dt = st_view.listChildren(include=['device tree'])[0]

st_root_category = get_category_by_path(st_dt, args.device_path)

if not st_root_category:
    if args.verbose:
        print('{path}: not found in siptrack'.format(
            path=args.device_path
        ), file=stderr)
    exit(1)

traverse_objects(st_root_category)

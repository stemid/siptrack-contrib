#!/usr/bin/env python
# coding: utf-8
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


def search_objects(st_object):
    total_values = 0
    found_values = 0

    args = parser.parse_args()

    search_classes = []
    try:
        search_classes = _classes[args.object_type]['class types']
    except KeyError:
        pass

    for node in st_object.traverse(max_depth=args.max_depth, include=search_classes):
        total_values += 1
        if node.class_id != args.object_type:
            continue
        if node.attributes.get(args.attribute_name, False):
            continue

        attribute = node.attributes.get(args.attribute_name, '')
        if fnmatch(attribute, args.attribute_value):
            found_values += 1
            print('{oid};{name};{attr};{val};'.format(
                oid=node.oid,
                name=node.attributes.get('name', 'UNKNOWN'),
                attr=args.attribute_name,
                val=attribute
            ))

    return total_values, found_values


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
    default=None,
    dest='device_path',
    help=('Path to the device category to use as root for the import. '
          'Separate path components with : (semicolon) by default.'
          'Example: -d \'Public Cloud:Devices\'')
)

parser.add_argument(
    '-m', '--max-depth',
    default=16,
    help='Maximum recursive depth for searching'
)

parser.add_argument(
    '--no-csv-header',
    action='store_true',
    help='Disable CSV header'
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
    default='?*',
    help=('Attribute value to search for, takes wildcards like fnmatch. '
          'Default will list any non-empty name attribute.')
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

if args.device_path:
    st_root = get_category_by_path(st_dt, args.device_path)
else:
    st_root = st_view

if not st_root:
    if args.verbose > 1:
        print('{path}: not found in siptrack'.format(
            path=args.device_path
        ), file=stderr)
    exit(1)

if not args.no_csv_header:
    print('oid;name;attribute;value;')

total_values, found_values = search_objects(st_root)

if args.verbose:
    print('Found {found} out of {total} values searched'.format(
        found=found_values,
        total=total_values
    ))

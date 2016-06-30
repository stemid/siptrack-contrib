# coding: utf-8
# REPL loaded with Siptrack connection.
#
# Run like: ipython -i -- repl.py --config siptrack_local.cfg
# by Stefan Midjich <swehack@gmail.com> - 2015

from argparse import ArgumentParser
from ConfigParser import RawConfigParser
from pprint import pprint as pp

import siptracklib
import siptracklib.errors

parser = ArgumentParser()
config = RawConfigParser()

def st_connect():
    args = parser.parse_args()
    config.readfp(args.configuration)

    st = siptracklib.connect(
        config.get('siptrack', 'hostname'),
        config.get('siptrack', 'username'),
        config.get('siptrack', 'password'),
        config.get('siptrack', 'port'),
        use_ssl=config.getboolean('siptrack', 'ssl')
    )

    return(st)

# TODO: Under construction 🏗 
def st_refresh():
    siptracklib.cm.disconnect()
    return(st_connect())


parser.add_argument(
    '-v', '--verbose',
    action='count',
    default=False,
    dest='verbose',
    help='Verbose output, use more v\'s to increase level'
)

parser.add_argument(
    '-c', '--configuration',
    type=file,
    required=True,
    help='Configuration with siptrack connection credentials'
)

st = st_connect()

st_view = st.view_tree.getChildByName(
    config.get('siptrack', 'base_view'),
    include=['view']
)

st_local_users = st.view_tree.user_manager.listChildren(include=['user local'])
st_passtree = st_view.listChildren(include=['password tree'])[0]
session_user = st.getSessionUser()
device_tree = st_view.listChildren(include=['device tree'])[0]
user_manager = st.view_tree.user_manager

print(
    '''Available pre-defined variables:
    pp = pprint() alias
    st = {st}
    st_view = {st_view}
    device_tree = {device_tree}
    st_local_users = {st_local_users}
    st_passtree = {st_passtree}
    session_user = {session_user}
    user_manager = {user_manager}
    '''.format(
        st=st,
        st_view=st_view,
        st_local_users=st_local_users,
        st_passtree=st_passtree,
        session_user=session_user,
        device_tree=device_tree,
        user_manager=user_manager
    )
)

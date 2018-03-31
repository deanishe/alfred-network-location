#!/usr/bin/python
# encoding: utf-8
#
# Copyright (c) 2014 deanishe@deanishe.net
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-06-17
#

"""List, filter and activate network locations from within Alfred."""

from __future__ import print_function

import argparse
from collections import namedtuple
import re
import sys


from workflow import Workflow3, ICON_NETWORK, ICON_WARNING
from workflow.util import run_command

HELP_URL = 'https://github.com/deanishe/alfred-network-location/issues'
ICON_UPDATE = 'update.png'
UPDATE_SETTINGS = {
    'github_slug': 'deanishe/alfred-network-location'
}


log = None
decode = None
match = re.compile(r'([ *]+)([0-9A-F-]+)\s\((.+)\)').match


Location = namedtuple('Location', 'name id current')


def get_locations():
    """Return list of available network locations."""
    locations = []

    cmd = ['/usr/sbin/scselect']
    output = decode(run_command(cmd))
    for line in output.split('\n'):
        m = match(line)
        if not m:
            continue

        state, id_, name = [s.strip() for s in m.groups()]
        state = True if state else False
        loc = Location(name, id_, state)
        log.debug('%r', loc)
        locations.append(loc)

    return locations


def do_list_locations(query=None):
    """Display list of available locations in Alfred."""
    if not query and wf.update_available:  # show update
        wf.add_item('An Update is Available',
                    u'↩ or ⇥ to install',
                    valid=False,
                    autocomplete='workflow:update',
                    icon=ICON_UPDATE)

    locations = wf.cached_data('locations', get_locations, session=True)

    if query:
        locations = wf.filter(query, locations, key=lambda loc: loc.name)

    for loc in locations:

        if loc.current:
            title = loc.name + u' (active)'
            subtitle = u'This location is currently active'
            valid = False

        else:
            title = loc.name
            subtitle = u'Switch to this location'
            valid = True

        wf.add_item(title, subtitle, valid=valid, arg=loc.id,
                    icon=ICON_NETWORK)

    wf.warn_empty('No matching network locations', 'Try a different query')
    wf.send_feedback()


def do_set_location(name):
    """Change to location ``name``."""
    run_command(['/usr/sbin/scselect', name])
    print(name.encode('utf-8'), end='')
    wf.clear_session_cache()


def main(wf):
    """Run Script Filter."""
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('list', 'set'))
    parser.add_argument('query', nargs='?')
    args = parser.parse_args(wf.args)

    log.debug('action=%r, query=%r', args.action, args.query)

    if args.action == 'list':
        return do_list_locations(args.query)
    elif args.action == 'set':
        return do_set_location(args.query)


if __name__ == '__main__':
    wf = Workflow3(
        help_url=HELP_URL,
        update_settings=UPDATE_SETTINGS,
    )
    log = wf.logger
    decode = wf.decode
    sys.exit(wf.run(main))

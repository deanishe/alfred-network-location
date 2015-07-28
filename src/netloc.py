#!/usr/bin/python
# encoding: utf-8
#
# Copyright © 2014 deanishe@deanishe.net
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-06-17
#

"""
List, filter and activate network locations from within Alfred
"""

from __future__ import print_function, unicode_literals

import sys
import subprocess
import argparse

from workflow import Workflow, ICON_NETWORK, ICON_WARNING

VERSION = '1.0'

MAX_CACHE_AGE = 10  # seconds

log = None
decode = None


def get_locations():
    """Return list of available network locations"""
    cmd = ['networksetup', '-listlocations']
    output = decode(subprocess.check_output(cmd))
    return [l.strip() for l in output.split('\n') if l.strip()]


def get_current_location():
    """Return name of active network location"""
    cmd = ['networksetup', '-getcurrentlocation']
    return decode(subprocess.check_output(cmd)).strip()


def do_list_locations(wf, query=None):
    """Display list of available locations in Alfred"""
    locations = wf.cached_data('locations', get_locations,
                               max_age=MAX_CACHE_AGE)

    current_location = get_current_location()

    if query:
        locations = wf.filter(query, locations)

    modifier_subtitles = {'cmd': 'Open Network preferences'}

    if not locations:
        wf.add_item('No matching network locations',
                    'Try a different query',
                    icon=ICON_WARNING)

    else:
        for loc in locations:
            if loc == current_location:
                # title = '✅ {}'.format(loc)
                title = '{} (active)'.format(loc)
                subtitle = 'This location is currently active'
                valid = False
            else:
                title = loc
                subtitle = 'Action to switch to this location'
                valid = True
            wf.add_item(title, subtitle, modifier_subtitles,
                        valid=valid, arg=loc, icon=ICON_NETWORK)

    wf.send_feedback()


def do_set_location(wf, location):
    """Change to location ``location``"""
    subprocess.call(['/usr/sbin/networksetup', '-switchtolocation', location],
                    stdout=subprocess.PIPE)
    print(location.encode('utf-8'), end='')


def main(wf):
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('list', 'set'))
    parser.add_argument('query', nargs='?')
    args = parser.parse_args(wf.args)

    log.debug('action : {!r}  query : {!r}'.format(args.action, args.query))

    if args.action == 'list':
        return do_list_locations(wf, args.query)
    elif args.action == 'set':
        return do_set_location(wf, args.query)

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    decode = wf.decode
    sys.exit(wf.run(main))

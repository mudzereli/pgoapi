#!/usr/bin/env python
"""
pgoapi - Pokemon Go API
Copyright (c) 2016 tjado <https://github.com/tejado>
Modifications Copyright (c) 2016 j-e-k <https://github.com/j-e-k>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.

Author: tjado <https://github.com/tejado>
Modifications by: j-e-k <https://github.com/j-e-k>
"""

import os
import re
import json
import struct
import logging
import requests
import argparse
from time import sleep
from pgoapi import PGoApi
from pgoapi.utilities import f2i, h2f
from pgoapi.location import getNeighbors

from google.protobuf.internal import encoder
from geopy.geocoders import GoogleV3
from s2sphere import CellId, LatLng

cdarkgray = '\033[1;30m'
cblack = '\033[0;30m'
cred = '\033[1;31m'
cdarkred = '\033[0;31m'
cgreen = '\033[1;32m'
cdarkgreen = '\033[0;32m'
cyellow = '\033[1;33m'
cdarkyellow = '\033[0;33m'
cblue = '\033[1;34m'
cdarkblue = '\033[0;34m'
cmagenta = '\033[1;35m'
cdarkmagenta = '\033[0;35m'
ccyan = '\033[1;36m'
cdarkcyan = '\033[0;36m'
cgray = '\033[0;37m'
cwhite = '\033[1;37m'
cdefault = '\033[0;39m'

log = logging.getLogger(__name__)
from threading import Thread
from Queue import Queue
def get_pos_by_name(location_name):
    geolocator = GoogleV3()
    loc = geolocator.geocode(location_name)

    log.info(cdarkyellow + 'Your given location:' + cyellow + ' %s' + cdefault, loc.address.encode('utf-8'))
    log.info(cdarkyellow + 'lat/long/alt:' + cyellow + ' %s %s %s', loc.latitude, loc.longitude, loc.altitude)

    return (loc.latitude, loc.longitude, loc.altitude)

def init_config():
    parser = argparse.ArgumentParser()
    config_file = "config.json"

    # If config file exists, load variables from json
    load = {}
    if os.path.isfile(config_file):
        with open(config_file) as data:
            load.update(json.load(data))

    # Read passed in Arguments
    required = lambda x: not x in load['accounts'][0].keys()
    parser.add_argument("-i", "--config_index", help="Index of account in config.json", default=0, type=int)
    parser.add_argument("-l", "--location", help="Location", required=required("location"))
    parser.add_argument("-d", "--debug", help="Debug Mode", action='store_true', default=False)
    config = parser.parse_args()
    load = load['accounts'][config.__dict__['config_index']]
    # Passed in arguments shoud trump
    for key,value in load.iteritems():
        if key not in config.__dict__ or not config.__dict__[key]:
            config.__dict__[key] = value
    if config.auth_service not in ['ptc', 'google']:
      log.error(cred + "Invalid Auth service specified! ('ptc' or 'google')" + cdefault)
      return None

    return config.__dict__

def main():
    # log settings
    # log format
    logging.basicConfig(level=logging.INFO, format=cgray + '%(asctime)s : [' + ccyan + '%(module)s' + cgray + '] : [' + cyellow + '%(levelname)s' + cgray + '] >' + cwhite + ' %(message)s')
    # log level for http request class
    logging.getLogger("requests").setLevel(logging.WARNING)
    # log level for main pgoapi class
    logging.getLogger("pgoapi").setLevel(logging.INFO)
    # log level for internal pgoapi class
    logging.getLogger("rpc_api").setLevel(logging.INFO)

    config = init_config()
    if not config:
        return

    if config["debug"]:
        logging.getLogger("requests").setLevel(logging.DEBUG)
        logging.getLogger("pgoapi").setLevel(logging.DEBUG)
        logging.getLogger("rpc_api").setLevel(logging.DEBUG)

    position = get_pos_by_name(config["location"])

    # instantiate pgoapi
    pokemon_names = json.load(open("pokemon.en.json"))
    api = PGoApi(config, pokemon_names)

    # provide player position on the earth
    api.set_position(*position)

    # retry login every 30 seconds if any errors
    while not api.login(config["auth_service"], config["username"], config["password"]):
        log.error('Retrying Login in 30 seconds')
        sleep(30)

    # main loop
    while True:
        try:
            api.main_loop()
        except Exception as e:
            log.error(cred + 'Error in main loop, restarting %s' + cdefault, e)
            # restart after sleep
            sleep(30)
            main()

if __name__ == '__main__':
    main()

#!/usr/bin/python
# -*- coding: utf-8 -*-


################################################################################
#                                                                              #
# This script creates restful API service to convert UTM and MGRD to lat       #
# and long coordinates.                                                        #
# IT can be used to support Openrefine projects                                #
#                                                                              #
# Creator: Rui Figueira                                                        #
###############################################################################

# To use,run with
#
# python app_utm.py
#
# and open browser at
#
# http://127.0.0.1:5000/utm
# or
# http://127.0.0.1:5000/mgrs


import json
import utm
import mgrs
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def help():
    return "<!DOCTYPE html><html><h2>API UTM conversion</h2><p>This API returns "\
    "coordinate transformations between UTM coordinates and geographic coordinates. "\
    "It assumes the same input and output coordinate reference system.</p><h2>"\
    "How to use:</h2><h3>Convert from UTM easting and northings</h3><p><code>"\
    "http://127.0.0.1:5000/fromUTM?eastings=VALUE&northings=VALUE&zone_number=VALUE&zone_letter=VALUE</code>."\
    "</p><p>Example: <a href=\"http://127.0.0.1:5000/fromUTM?eastings=414278&"\
    "northings=5316285&zone_number=32&zone_letter=S\">http://127.0.0.1:5000/"\
    "fromUTM?eastings=414278&northings=5316285&zone_number=32&zone_letter=S</a>"\
    "</p><h3>Convert from latitude and longitude to UTM easting and northings"\
    "</h3><p><code>http://127.0.0.1:5000/toUTM?lat=VALUE&long=VALUE</code>.</p> "\
    "<p>Example: <a href=\"http://127.0.0.1:5000/toUTM?lat=41.9350330&long=-6.75523\">"\
    "http://127.0.0.1:5000/toUTM?lat=41.9350330&long=-6.75523</a></p><h3>Convert from MGRS"\
    "</h3><p><code>http://127.0.0.1:5000/fromMGRS?mgrs=VALUE</code>.</p><p>Example: "\
    "<a href=\"http://127.0.0.1:5000/fromMGRS?mgrs=29TPG861450\">http://127.0.0.1:5000/"\
    "mgrs?mgrs=29TPG861450</a></p><h3>Convert to MGRS</h3><p><code>http://127.0.0.1:5000/"\
    "toMGRS?lat=VALUE&long=VALUE</code>.</p><p>Example: <a href=\"http://127.0.0.1:5000/"\
    "toMGRS?lat=41.9350330&long=-6.75523\">http://127.0.0.1:5000/toMGRS?lat=41.9350330&long=-6.75523</a></p></html>"

# define path to get lat long from eastings and northings
@app.route('/fromUTM', methods=['GET'])
def utm_to_latlong():
    eastings = request.args.get('eastings')
    northings = request.args.get('northings')
    zone_number = request.args.get('zone_number')
    zone_letter = request.args.get('zone_letter')

# cast to make sure params are in correct type
    e = int(eastings)
    n = int(northings)
    zn = int(zone_number)
    zl = str(zone_letter)

# debug type of params
    print('e type: {}, n type: {}, zn type: {}, zl type: {}'.format(type(e),
        type(n), type(zn), type(zl)))

# create tupple wit params
    u = (e, n, zn, zl)
    print(type(u))

    c = utm.to_latlon(*u)
    return '''
        {}'''.format(c)

# define path to get eastings and northings from lat long
@app.route('/toUTM', methods=['GET'])
def latlong_to_utm():
    lat = request.args.get('lat')
    long = request.args.get('long')

#cast to make sure params are in correct type
    rlat = float(lat)
    rlong = float(long)
    print('lat {}, long {}'.format(rlat, rlong))
    print('lat type: {}, long type: {}'.format(type(rlat), type(rlong)))

    c = utm.from_latlon(rlat, rlong)
    return '''
        {}'''.format(c)


# define path to get lat lon from mgrs
@app.route('/fromMGRS', methods=['GET'])
def mgrs_to_latlong():
    grid = request.args.get('mgrs')

#cast to make sure params are in correct type
    c = str(grid)
    print('coord: {}'.format(c))
    print('coord type: {}'.format(type(c)))

    #coord = '29TPG861450'
    m = mgrs.MGRS()

    p = m.toLatLon(c)
    return '''
        {}'''.format(p)

# define path to get mgrs from lat long
@app.route('/toMGRS', methods=['GET'])
def latlong_to_mgrs():
    lat = request.args.get('lat')
    long = request.args.get('long')

#cast to make sure params are in correct type
    rlat = float(lat)
    rlong = float(long)
    print('lat {}, long {}'.format(rlat, rlong))
    print('lat type: {}, long type: {}'.format(type(rlat), type(rlong)))

    m = mgrs.MGRS()

    p = m.toMGRS(rlat, rlong)
    return '''
        {}'''.format(p)


if __name__ == '__main__':
    app.run(debug=True, port = 5000)

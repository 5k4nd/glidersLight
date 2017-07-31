#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
littleDad, august 2016.


> get all informations you need about your specific aircraft on http://live.glidernet.org/

DOC :
    http://wiki.glidernet.org/wiki:ogn-python


machines :
    F-CECK  DDB11C
    DDB223  DD9981
            DDAFBD
    F-CEAA  DDB223



ToDo:
- comparer la position avec la distance à LFNC

- faire une interface Flask avec entrée du 'real_address' puis 'address' si le premier est inconnu (c'est souvent le cas !)
- ajout de l'autocomplétion sur les champs précédents

- tous les planeurs sur un fond OSM en js sur glider.baptabl.fr


"""

from ogn.client import AprsClient
from ogn.parser import parse_aprs, parse_ogn_beacon, ParseError
from geopy.distance import vincenty

from os import system
from redis import Redis
import json

class variables():
    temp_test = (44.74828, 6.58068)
    piste_nord = (44.70542, 6.59794)
    piste_sud = (44.69882, 6.60120)
    miche = (44.70388, 6.60025)
    current_tracked = 'DDB223'



def niceprint_beacon(beacon):

    system('clear')

    clean_beacon = { arg: beacon[arg] for arg in \
        [
            'address',
            # 'address_type',
            # 'aircraft_type',
            'altitude',
            # 'beacon_type',
            'climb_rate',
            # 'comment',
            # 'error_count',
            # 'flightlevel',
            'frequency_offset',
            # 'gps_status',
            'ground_speed',
            # 'hardware_version',
            'latitude',
            'longitude',
            'name',
            'real_address',
            'receiver_name',
            'signal_power',
            'signal_quality',
            # 'software_version',
            'stealth',
            # 'symbolcode',
            # 'symboltable',
            'track',
            'turn_rate',
        ]
    }

    # print('Aircraft: {name}\nalt: {altitude}'.format(**beacon))
    for arg, value in clean_beacon.items():
        print(arg + ': ' + str(beacon[arg]))


def gliderlight_process(beacon):
    """
        extrait les données interéssantes du beacon (nom, latitude, longitude)
        et stocke le tout dans un json applati (flat) sur redis/localhost
    """
    print("process beacon")
    raw_data = r.get("glidersLight")
    if not(raw_data is None):  # empty redis
        data = json.loads(raw_data)
    else:
        data = {}
        data[beacon['address']] = (beacon['latitude'], beacon['longitude'])
        r.set("glidersLight", json.dumps(data))

def process_beacon(raw_message):
    if raw_message[0] == '#':
    #     print('Server Status: {}'.format(raw_message))
        return

    try:
        beacon = parse_aprs(raw_message)
        beacon.update(parse_ogn_beacon(beacon['comment']))

        if beacon['beacon_type'] == 'aircraft_beacon':
            # if beacon['receiver_name'] == 'CSS4':
            if beacon['receiver_name'] == 'LFNF':
            # if beacon['address'] == variables.current_tracked:
                gliderlight_process(beacon)
                # niceprint_beacon(beacon)
    except ParseError as e:
        # print('Error, {}'.format(e.message))
        pass


def start_client():
    print("RUNNING: ogn client")
    global r
    r = Redis('localhost')
    client = AprsClient(aprs_user='N0CALL')
    client.connect()
    return client


if __name__ == '__main__':
    client = start_client()
    try:
        client.run(callback=process_beacon, autoreconnect=True)
    except KeyboardInterrupt:
        print('\nStop ogn gateway')
        client.disconnect()





    exit(1)

    # print(int(vincenty(piste_sud, piste_nord).meters))
    # cur_lat = format(test_latitude, '.5f')
    # cur_long = format(test_longitude, '.5f')





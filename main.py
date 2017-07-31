#!/usr/bin/env python3
# coding: utf-8

"""
Todo:
- stocker les variables dans ogn_tracker via redis, ATTENTION après avoir récupéré les anciennes
- les utiliser dans glidersLight 


import redis
conn = redis.Redis('localhost')

user = {"Name":"Pradeep", "Company":"SCTL", "Address":"Mumbai", "Location":"RCP"}

conn.hmset("pythonDict", user)

conn.hgetall("pythonDict")
    
    {'Company': 'SCTL', 'Address': 'Mumbai', 'Location': 'RCP', 'Name': 'Pradeep'}


"""



############ Flask part
#################################

from flask import Flask, jsonify
app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5559'
app_name = 'Saint-Crépin in the Sky'

from multiprocessing import Process
from ogn_tracker_v01 import start_client, process_beacon

import json
from redis import Redis

def run_server():
    app.run()
        



@app.route('/', methods=['GET'])
def get_geojson_data():
    redis_data = r.get("glidersLight")
    if not(redis_data is None):
        decoded_data = json.loads(redis_data)
        # return(str(json.loads(redis_data)))
        return """{"geometry": {"type": "Point", "coordinates": %s}, "type": "Feature", "properties": {}}""" % decoded_data['DD9981']
    else:
        return "{}" 



def geojson_processing(beacon):
    variables.geojson_data = """
    {"geometry":
    {
        "type": "Point", "coordinates": [%s, %s]
    },
    "type": "Feature", "properties": {}
    }""" % (beacon['latitude'], beacon['longitude'])

    print("geojson_data UPDATED\n")






if __name__ == "__main__":
    r = Redis('localhost')
    server = Process(target=app.run)
    server.start()

    client = start_client()
    try:
        client.run(callback=process_beacon, autoreconnect=True)
    except KeyboardInterrupt:
        print('\nAttente de terminaison.')
        pass

    print("KILLING: serveur flask")
    server.terminate()
    server.join()
    
    client.disconnect()
    print('\nTERMINÉ.')








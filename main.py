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
from ogn_tracker import start_client, process_beacon

import json
from redis import Redis

def run_server():
    app.run()
        




tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/tasks', methods=['GET'])
def get_geojson_data():
    redis_data = r.get("glidersLight")
    if not(redis_data is None):
        return jsonify(json.loads(redis_data))
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


# @app.route('/')
# def hello_world():
#     # return """{"geometry": {"type": "Point", "coordinates": [149.15878697788955, -48.881527700957491]}, "type": "Feature", "properties": {}}"""
#     return str(variables.geojson_data)








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







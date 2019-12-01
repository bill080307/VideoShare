#!/usr/bin/python3
import ipfshttpclient
import json
import os
import redis

api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001', timeout=1200)
path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'data')
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


def loadjson(jsonfile):
    with open(jsonfile) as json_file:
        data = json.load(json_file)
        return data


if __name__ == '__main__':
    files = os.listdir(path)
    for item in files:
        if item == 'videoshare.json':
            data = loadjson(os.path.join(path, item))
            for k1, v1 in data['users'].items():
                h = api.name.resolve(v1)
                r.set(v1, h['Path'][6:])
                r.set(k1, h['Path'][6:])
            for k1, v1 in data['global'].items():
                h = api.name.resolve(v1)
                r.set(v1, h['Path'][6:])
                r.set(k1, h['Path'][6:])
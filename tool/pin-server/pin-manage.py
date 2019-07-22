#!/usr/bin/python3
import ipfshttpclient
import json
import os
import pika

api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001', timeout=1200)
path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'data')

username = 'guest'
pwd = 'guest'
user_pwd = pika.PlainCredentials(username, pwd)
s_conn = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1', credentials=user_pwd))

chan = s_conn.channel()
chan.queue_declare(queue='ipfspin', durable=True)


def loadjson(jsonfile):
    with open(jsonfile) as json_file:
        data = json.load(json_file)
        return data


def getpinhash():
    mylist = []
    templist = api.pin.ls(type='recursive')
    for item in templist['Keys']:
        mylist.append(item)
    return mylist


def getmyhash():
    mylist = []
    files = os.listdir(path)
    for item in files:
        if item == 'parameters.json':
            data = loadjson(os.path.join(path, item))
            for k1, v1 in data.items():
                mylist.append(v1['cid'])
    return mylist


def ipfsrmpin(lists):
    for item in lists:
        print(item)
        api.pin.rm(item)


def ipfsaddpin(lists):
    for item in lists:
        print(item)
        # api.pin.add(item)
        chan.basic_publish(exchange='', routing_key='ipfspin', body=item,
                           properties=pika.BasicProperties(delivery_mode=2))
    s_conn.close()


if __name__ == '__main__':
    localhash = getpinhash()
    pinhash = getmyhash()

    rmpinhash = list(set(localhash).difference(set(pinhash)))
    downloadpinhash = list(set(pinhash).difference(set(localhash)))

    print(localhash)
    print(pinhash)
    print(rmpinhash)
    ipfsrmpin(rmpinhash)
    print(downloadpinhash)
    ipfsaddpin(downloadpinhash)
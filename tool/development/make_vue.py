#!/usr/bin/python3
import json
import ipfshttpclient
import os

api = ipfshttpclient.connect('/ip4/172.16.1.8/tcp/5001', timeout=1200)


def tohash(path):
    os.chdir(path)
    os.system('npm run build')
    hash = api.add(os.path.join(path, 'dist'), recursive=True)
    return hash[-1]


def loadjson(jsonfile):
    with open(jsonfile, 'r+', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data


def writejson(jsonfile, jsonvalue):
    with open(jsonfile, "w", encoding='utf-8') as json_file:
        json_file.write(json.dumps(jsonvalue, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    path = os.path.split(os.path.realpath(__file__))[0]
    path = os.path.abspath(os.path.join(path, '..', '..'))
    playerhash = tohash(os.path.join(path, 'player'))
    videolisthash = tohash(os.path.join(path, 'videolist'))

    Gkey = {}
    keylist = api.key.list()
    for key in keylist['Keys']:
        if key['Name'] == 'VideoShareG':
            Gkey = key
    if Gkey == {}:
        Gkey = api.key.gen('VideoShareG', type='rsa')
    globalPath = os.path.join(path, 'home', 'public', 'global.json')
    globalJson = loadjson(globalPath)
    globalJson['id'] = Gkey['Id']
    writejson(globalPath, globalJson)
    globalhash = tohash(os.path.join(path, 'home'))

    temPath = os.path.join(path, 'dashboard', 'public', 'data.json')
    temJson = loadjson(temPath)

    temJson['template'] = {
        'global': globalhash['Hash'],
        'userlist': videolisthash['Hash'],
        'player': playerhash['Hash']
    }
    writejson(temPath, temJson)
    dashboardhash = tohash(os.path.join(path, 'dashboard'))

    print(dashboardhash)
    print('http://127.0.0.1:8080/ipfs/%s'%dashboardhash['Hash'])
    # api.name.publish(globalhash['Hash'], lifetime="720h", key='VideoShareG')
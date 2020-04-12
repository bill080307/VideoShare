#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import os
import ipfshttpclient
api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
path=u'/'

def upload(file):
    name = os.path.basename(file)
    print(name)
    res = api.add(file)
    cid = res['Hash']
    size = res['Size']
    output = os.popen(u'cd %s;ffprobe -v quiet -print_format json -show_format -show_streams %s' % (os.path.dirname(file), os.path.basename(file)))
    mediainfo = output.read()
    dictinfo = json.loads(mediainfo)
    duration = round(float(dictinfo['format']['duration']))
    res2 = {
        'title': name,
        'size': size,
        'duration': duration,
        'url': '/ipfs/%s' % cid,
        'mediainfo': dictinfo
    }
    return res2

cover = ''
files = []
if os.path.isdir(path):
    print('Dir')
    title = os.path.basename(path)
    if os.path.isfile(os.path.join(path, 'cover.jpg')):
        res = api.add(os.path.join(path, 'cover.jpg'))
        cover = res['Hash']
    vfiles = os.listdir(path)
    for file in vfiles:
        if os.path.isfile(os.path.join(path, file)):
            files.append(upload(os.path.join(path, file)))
    # print(files)
else:
    title = os.path.basename(path)
    (title, extension) = os.path.splitext(title)
    files.append(upload(path))
    # print(files)

out = {
    'title': title,
    'cover': cover,
    'files': files
}

file = open('%s.json' % title, 'w')
json.dump(out, file)
file.close()
res = api.add('%s.json' % title)
print(res['Hash'])

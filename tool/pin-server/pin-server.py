#!/usr/bin/python3
import ipfshttpclient
import pika
import time

username = 'guest'
pwd = 'guest'
api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001', timeout=1200)
user_pwd = pika.PlainCredentials(username, pwd)


def callback(ch, method, properties, body):
    print(body.decode('UTF-8'))
    try:
        api.pin.add(body.decode('UTF-8'))
    except:
        print("pin error")
    ch.basic_ack(delivery_tag=method.delivery_tag)


while True:
    try:
        s_conn = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1', credentials=user_pwd))
        chan = s_conn.channel()
        chan.queue_declare(queue='ipfspin', durable=True)

        chan.basic_qos(prefetch_count=1)
        chan.basic_consume(queue='ipfspin', on_message_callback=callback, auto_ack=False)
        chan.start_consuming()
    except:
        time.sleep(10)

# chan.basic_qos(prefetch_count=1)
# chan.basic_consume(queue='ipfspin', on_message_callback=callback, auto_ack=False)
# while True:
#    try:
#        chan.start_consuming()
#    except:
#        time.sleep(10)

'''

script for sending same message to multiple consumers.
'''
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

'''
fanout exchange type copies and routes a received message to all queues 
that are bound to it regardless of routing keys or pattern matching as 
with direct and topic exchanges. Keys provided will simply be ignored.

'''
channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')
counter = 0
while counter < 10000 :
    counter =counter+1
    message = "Hello World!"+ str(counter)

    # here we take exchange name and no routing key
    channel.basic_publish(exchange='logs',
                          routing_key='',
                          body=message,
                          )
    print(" [x] Sent %r" % message)

input()
connection.close()
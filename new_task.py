'''

Script to send durable and persistant messages to consumers.

'''

import pika
import sys


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# durable here is to make sure that the queue stay when rabbitmq server stops
channel.queue_declare(queue='task_queue', durable=True)
counter = 0


while counter < 100 :
    counter =counter+1
    message = "Hello World!"+ str(counter)
    # delivery mode here is to make sure that rabbitmq saves the data on disk

    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=message,
                          properties=pika.BasicProperties(
                             delivery_mode = 2, # make message persistent
                          ))
    print(" [x] Sent %r" % message)
connection.close()
'''

RabbitMQ program for recieveing messages

'''

import pika

'''

The BlockingConnection creates a layer on top of Pika’s asynchronous core
providing methods that will block until their expected response has returned.

Due to the asynchronous nature of the Basic.Deliver and Basic.Return calls 
from RabbitMQ to your application, you can still implement continuation-passing 
style asynchronous methods if you’d like to receive messages from RabbitMQ 
using basic_consume or if you want to be notified of a delivery failure when 
using basic_publish.

'''

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host = 'localhost'
))

# channel to interact with RabbitMQ
channel = connection.channel()

# to send data we specify the queue
'''
Declare queue, create if needed. This method creates or checks a queue. When 
creating a new queue the client can specify various properties that control 
the durability of the queue and its contents, and the level of sharing for 
the queue.

'''
channel.queue_declare(queue='hello')


def any_method_name(ch, method, properties, body):
    print("recieved")
    print(body)

'''
The method below asks the server to start a "consumer", which is a transient 
request for messages from a specific queue. Consumers last as long as the 
channel they were declared on, or until the client cancels them.


basic_consume of pika sends the AMQP command Basic.Consume to the broker and 
binds messages for the consumer_tag to the consumer callback. If you do not 
pass in a consumer_tag,one will be automatically generated for you. Returns 
the consumer tag.

parameters:-
    * consumer_callback (method) – The method to callback when consuming
    * queue (str or unicode) – The queue to consume from
    * no_ack (bool) – Tell the broker to not expect a response
    * exclusive (bool) – Don’t allow other consumers on the queue
    * consumer_tag (str or unicode) – Specify your own consumer tag
    * arguments (dict) – Custom key/value pair arguments for the consume

'''
channel.basic_consume(any_method_name, queue='hello', no_ack = True)

print('waiting for messages. To exit press ctrl+c')
# starts consuming from registered callbacks
channel.start_consuming()

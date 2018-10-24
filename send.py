import pika


connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')


'''
Publish to the channel with the given exchange, routing key and body. 
Returns a boolean value indicating the success of the operation.

Parameters:-
* exchange (str or unicode) – The exchange to publish to
* routing_key (str or unicode) – The routing key to bind on
* body (str or unicode) – The message body
* properties (pika.spec.Properties) – Basic.properties
* mandatory (bool) – The mandatory flag
* immediate (bool) – The immediate flag

'''
channel.basic_publish(exchange='', routing_key='hello'
                      , body='Hello World')
print("Sent Hello World!!")

# flush network buffers of any data
connection.close()

'''
script to recieve sent broadcast message. run file in different terminals to
see the broadcast.
'''
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

'''
once the consumer connection is closed, the queue should be deleted. 
The exclusive flag is for that purpose
'''
result = channel.queue_declare(exclusive=True)
# accessing via method output above
queue_name = result.method.queue

channel.queue_bind(exchange='logs',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

# no_ack makes sense as we do not need to know if log has reached.
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
'''

script to show how messages can be distributed to multiple consumers.
run this file on multiple terminals to see the whole exercise
'''

import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

'''
basic_ack:- Acknowledge one or more messages. 
When sent by the client, this method acknowledges one or more messages delivered 
via the Deliver or Get-Ok methods. 
When sent by server, this method acknowledges one or more messages published with
the Publish method on a channel in confirm mode. The acknowledgement can be for a 
single message or a set of messages up to and including a specific message.

'''
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

'''
Specify quality of service. This method requests a specific quality of service. 
The QoS can be specified for the current channel or for all channels on the 
connection. The client can request that messages be sent in advance so that when 
the client finishes processing a message, the following message is already held 
locally, rather than needing to be sent down the channel. 
Prefetching gives a performance improvement.

Parameters->
    * prefetch_count->
      Specifies a prefetch window in terms of whole messages. This field may be 
      used in combination with the prefetch-size field; a message will only be 
      sent in advance if both prefetch windows (and those at the channel and 
      connection level) allow it. The prefetch-count is ignored if the no-ack 
      option is set.

    * prefetch_size->This field specifies the prefetch window size. 
      The server will send a message in advance if it is equal to or smaller in 
      size than the available prefetch size (and also falls into other prefetch 
      limits). May be set to zero, meaning “no specific limit”, although other 
      prefetch limits may still apply. The prefetch-size is ignored if the no-ack 
      option is set.
'''
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()
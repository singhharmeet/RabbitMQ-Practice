import pika
import random

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# exchange type is direct hence routing key and binding key will
# be exact matched
channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')

severity = ["Debug", "Error", "Info"]
counter = 0

while counter < 100 :
    counter =counter+1
    message = "Hello World!"+ str(counter)
    # random severity level
    x = random.randint(0, 2)
    message  = severity[x]+message
    # routing key will be checked with binding key
    y = channel.basic_publish(exchange='direct_logs',
                          routing_key=severity[x],
                          body=message)
    print(y)
    print(" [x] Sent "+ message)
connection.close()
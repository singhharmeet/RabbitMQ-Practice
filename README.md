# RabbitMQ-Practice
For RabbitMQ Integration


# RabbitMQ

*  Occasionally, one needs to delay a time-consuming job for a while; it needs to be queued for future execution so that something more important can be dealt with. 
* For this to happen, you need a broker: someone who will accept messages (e.g. jobs, tasks) from various senders (i.e. a web application), queue them up, and distribute them to the relevant parties (i.e. workers) to make use of them - all asynchronously and on demand.
* ***Message Brokers*** are usually application stacks with dedicated pieces covering the each stage of the exchange setup. 
* From accepting a message to queuing it and delivering it to the requesting party, brokers handle the duty which would normally be much more cumbersome with non-dedicated solutions or simple hacks such as using a database, cron jobs, etc. 
* They simply work by dealing with queues which technically constitute infinite buffers, to put messages and pop-and-deliver them later on to be processed either automatically or by polling.
* RabbitMQ is a message broker. It accepts and forwards messages.
* RabbitMQ server serves by accepting and forwarding messages in queue and RabbitMQ client can be taken as senders and recievers


* ***WHY TO USE RABBITMQ?***
	* These message brooking solutions act like a middleman for various services (e.g. your web application). 
	* They can be used to greatly reduce loads and delivery times by web application servers since tasks, which would normally take quite bit of time to process, can be delegated for a third party whose sole job is to perform them (e.g. workers). 
	* They also come in handy when a more "guaranteed" persistence is needed to pass information along from one place to another.
	* Allowing web servers to respond to requests quickly instead of being forced to perform resource-heavy procedures on the spot
	* Distributing a message to multiple recipients for consumption (e.g. processing)
	* Letting offline parties (i.e. a disconnected user) fetch data at a later time instead of having it lost permanently
	* Introducing fully asynchronous functionality to the backend systems
	* Ordering and prioritising tasks
	* Balancing loads between workers
	* Greatly increase reliability and uptime of your application
* RabbitMQ-server service->
	* **start**- service rabbitmq-server start
	* **stop** - service rabbitmq-server stop
	*  **restart** - replace stop with restart
	*  **status** - replace stop with status
	*  to enable Rabbit MQ management console, run the following --> 
		* ```sudo rabbitmq-plugins enable rabbitmq_management```
		* access the above console by visiting http://<ip address>:15672/
		* username and password are both set to "guest"


***To see what queues RabbitMQ has and how many messages are in them:-***
```
sudo rabbitmqctl list_queues
```
***Standard RabbitMQ message flow***
* The producer publishes a message to the exchange.
* The exchange receives the message and is now responsible for the routing of the message.
* A binding has to be set up between the queue and the exchange.
* The exchange routes the message in to the queues.
* The messages stay in the queue until they are handled by a consumer
* The consumer handles the message.

***Some Terminology-***
* Producing->sending, producer-> send message program

* ***Queue*** is essentially a large message buffer that stores messages. A queue is bound by is host memory's limits.
* ***exchange*** on one side it receives messages from producers and the other side it pushes them to queues. 
	* A binding is a "link" that you set up to bind a queue to an exchange. It is relationship between exchange and a queue.
	* The routing key is a message attribute. The exchange might look at this key when deciding how to route the message to queues (depending on exchange type).
	* Exchanges, connections, and queues can be configured with parameters such as durable, temporary, and auto delete upon creation.
		* Durable exchanges survive server restarts and last until they are explicitly deleted. 
		* Temporary exchanges exist until RabbitMQ is shut down. 
		* Auto-deleted exchanges are removed once the last bound object unbound from the exchange.
	* The exchange must know exactly what to do with a message it receives. 	
	* Eg.->Should it be appended to a particular queue? Should it be appended to many queues? Or should it get discarded. 
	* In RabbitMQ, there are four different types of exchange that route the message differently using different parameters and bindings setups. 
	* Clients can create their own exchanges or use the predefined default exchanges
	* **Exchange types are-**
		* **direct-**
			* A direct exchange delivers messages to queues based on a message routing key. 
			* The routing key is a message attribute added into the message header by the producer. 
			* The routing key can be seen as an "address" that the exchange is using to decide how to route the message. 
			* A message goes to the queue(s) whose binding key exactly matches the routing key of the message.
		* **default-**
			* The default exchange is a pre-declared direct exchange with no name, usually referred by the empty string "". 
			* When you use the default exchange, your message is delivered to the queue with a name equal to the routing key of the message. 
			* Every queue is automatically bound to the default exchange with a routing key which is the same as the queue name.
		* **topic-**
			* Topic exchanges route messages to queues based on wildcard matches between the routing key and something called the routing pattern specified by the queue binding. 
			* Messages are routed to one or many queues based on a matching between a message routing key and this pattern.
		* headers
		* fanout


* Consuming->receiving messages, consumer-> mostly waits to receive messages
* _Producer, consumer and queue does not need to reside in same host._
* _An application can be both producer and consumer too._
* RabbitMQ uses AMQP 0.9.1 messaging protocol for messaging

* ***Hello World Example files->***
	* send.py github
	* recieve.py github


* * Competing consumers-> solves the question "how can a messaging client process multiple message concurrently?" by distributing queue messages to multiple consumers on recieveing(client) side.

### Work Queues-
* in Rabbit MQ, to achieve  the above(distributing different, time consuming task among multiple workers), we create ***Work Queue(aka Task Queues)*** .
*  ***Acknowledgement-***
	* In order to make sure a message is never lost, RabbitMQ supports message acknowledgments. An ack(nowledgement) is sent back by the consumer to tell RabbitMQ that a particular message had been received, processed and that RabbitMQ is free to delete it.
	* If a consumer dies (its channel is closed, connection is closed, or TCP connection is lost) without sending an ack, RabbitMQ will understand that a message wasn't processed fully and will re-queue it. 
	* If there are other consumers online at the same time, it will then quickly redeliver it to another consumer. ***That way you can be sure that no message is lost, even if the workers occasionally die.***
	* There aren't any message timeouts; RabbitMQ will redeliver the message when the consumer dies. It's fine even if processing a message takes a very, very long time.
	* Acknowledgement must be sent on the same channel the delivery it is for was received on. Attempts to acknowledge using a different channel will result in a channel-level protocol exception
	* _Manual message acknowledgements are turned on by default._

* ***Message Durability***-
	* this is to make sure that the messages aren't lost ***when RabbitMQ server stops*** .
	* RabbitMQ doesn't allow you to redefine an existing queue with different parameters and will return an error to any program that tries to do that. If you need to really change the parameters then you can do the following->
	```
channel.queue_delete(queue=<queue_name>)
	```
	* and create a new queue with same name(or don't delete and create new queue) and add settings to make queue "durable" and persist the messages.
	* Messages marked as 'persistent' that are delivered to 'durable' queues will be logged to disk. 
	* Durable queues are recovered in the event of a crash, along with any persistent messages they stored prior to the crash.
	* So you need to declare queue as durable (or it will be dropped after broker stops)



* ***Fair Dispatch -*** 
	* normally RabbitMQ dispatches messages evenly between consumers one by one(round robin dispatching).
	* for the problems where multiple messages with varying load is present, we can use the ```basic.qos``` method with the ```prefetch_count=1``` setting. 
	* This tells RabbitMQ not to give more than one message to a worker at a time. Or, in other words, don't dispatch a new message to a worker until it has processed and acknowledged the previous one. Instead, it will dispatch it to the next worker that is not still busy.
	

* ***Temporary Queues***-
	* Giving a queue a name is important when you want to share the queue between producers and consumers.
	* For cases where We want to hear about all messages, not just a subset of them. We're also interested only in currently flowing messages not in the old ones, we need temporary queues. 
	* To solve that we need two things. 
		* a queue with a random name, or, even better - let the server choose a random queue name for us. 
		* once the consumer connection is closed, the queue should be deleted. There's an exclusive flag for that
	


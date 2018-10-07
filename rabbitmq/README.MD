# RabbitMq Service

The RabbitMq service will be hold the tasks sended by the WebServer. Those tasks in the 
Rabbit queue will be processed by the cellery workers.

To run Rabbit service you need to get Docker installed on your system.

```sh
docker run -d --name cloud_rabbit \
	-e RABBITMQ_DEFAULT_USER=aucarvideo \
	-e RABBITMQ_DEFAULT_PASS=aucarvideo \
	-e RABBITMQ_DEFAULT_VHOST=aucarvideo
	rabbitmq:3


```

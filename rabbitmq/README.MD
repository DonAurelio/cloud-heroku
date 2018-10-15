# RabbitMq Service

The RabbitMq service will be hold the tasks sended by the WebServer. Those tasks in the 
Rabbit queue will be processed by the celery workers.

## Requirements

1. Deployment: Docker

## Deployment

To run Rabbit service you need to get Docker installed on your system.

```sh
docker run -d --name aucar_rabbit \
	-e RABBITMQ_DEFAULT_USER=aucar \
	-e RABBITMQ_DEFAULT_PASS=aucar \
	-e RABBITMQ_DEFAULT_VHOST=aucar \
	-p 8020:15672 \
	-p 8021:5672 \
	rabbitmq:3-management
```

Get the Rabbitmq monitoring GUI:

* Using the conainer http://container-ip:15672
* Using the host http://host-ip:8020 or http://localhost:8020. 

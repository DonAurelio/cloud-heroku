# RabbitMq Service

The RabbitMq service will be hold the tasks sended by the WebServer. Those tasks in the 
Rabbit queue will be processed by the celery workers.

## Requirements

1. Development: docker.io
2. Production: docker.io

## Run in Development and AWS

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

* Rabbitmq management GUI app port 15672
* Rabbitmq broker port 5672
* You can access management GUI by visiting http://container-ip:15672 in a browser or, if you need access outside the host, on port 8020.
* Or can then go to http://localhost:8020 or http://host-ip:8020 in a browser.

## Install Docker and docker-compose in AWS 

Install Docker and docker-compose in the WS instance.

```sh
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

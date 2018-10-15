# Celery Worker Service

The cellery worker is resposible for processing the videos placed in the nfs folder by the WebService. 

## Requirements

1. Development: Docker
2. Production: Docker, nfs-utils

## Run in Development

```sh
docker build -t aucar_worker .
```
Export the **BROKER_IP**

```sh
export BROKER_IP="$(docker inspect -f "{{ .NetworkSettings.Networks.bridge.IPAddress }}" aucar_rabbit)"
```
Run the worker container and set the **BROKER_URL**, **WEB_IP** and **WEB_PORT** env variables.

```sh
docker run --name aucar_worker \
	-e BROKER_URL="pyamqp://aucar:aucar@${BROKER_IP}:5672/aucar" \
	-e WEB_IP="<web-app-ip>" \
	-e WEB_PORT="<web-app-port>" \
	-v ${PWD}/supervisor/conf.d/:/etc/supervisor/conf.d/ \
	-v ${PWD}/supervisor/logs/:/home/app/logs/ \
	-v ${PWD}/../web/aucarvideo:/home/app/nfs \
	-p 8030:5555 \
	aucar_worker
```

BROKER_URL has the following format:

```sh
'pyamqp://${BROKER_PASS}:${BROKER_USER}@${BROKER_IP}:${BROKER_PORT}/${BROKER_VHOST}'
```

Get the Celery Flower monitoring GUI:

* Using the container http://container-ip:5555
* Using the host http://host-ip:8030 or localhost:8030.

## Run in AWS

On this deployment the nfs folder is mounted on the AWS EC2 instance an shared with the container through a volume.

### Configure AWS instance NFS

```sh
sudo yum install -y nfs-utils
```

Edit the /etc/hosts file of the WS instance and place at the end the private IPv4 Address of te FS service.

```sh
<ip_of_file_server_instance> 	nfs
```

Mount the FS shared directory and map that remote directory with the **media** folder on the web application.

```sh
sudo mount -t nfs nfs:/etc/nfs /etc/nfs
```

Edit the /etc/fstab and add the line below to mount the FS shared directory every time the instance starts up. 

```sh
nfs:/etc/nfs /etc/nfs	nfs	rw,sync,hard,intr	0	0
```

### Run the Worker in a Docker Container

Exporrt the worker AWS instace env variables

```sh
export WEB_IP="ip-web"
export WEB_PORT="port-web"
export BROKER_IP="ip-broker"
export BROKER_PORT=5672
export BROKER_VHOST=aucar
export BROKER_USER=aucar
export BROKER_PASS=aucar
```

Run the container that will use the env variables defined on the AWS instance

```sh
docker run -it --name aucar_worker \
	-e BROKER_URL="pyamqp://${BROKER_PASS}:${BROKER_USER}@${BROKER_IP}:${BROKER_PORT}/${BROKER_VHOST}" \
	-e WEB_IP=${WEB_IP} \
	-e WEB_PORT=${WEB_PORT} \
	-v ${PWD}/supervisor/conf.d/:/etc/supervisor/conf.d/ \
	-v ${PWD}/supervisor/logs/:/home/app/logs/ \
	-v /etc/nfs:/home/app/nfs \
	-p 8030:5555 \
	aucar_worker
```

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

# References

[Supervisor and Celery](https://medium.com/@channeng/celery-scheduler-part-2-managing-celery-with-supervisor-2a0c6e7f7a6e)


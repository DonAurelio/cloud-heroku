# Celery Worker Service

The cellery worker is resposible for processing the videos placed in the nfs folder by the WebService. 

## Requirements

1. Development: Docker
2. Production: Docker, nfs-utils

## Run in Development

```sh
docker build -t aucar_worker .
```

```sh
export BROKER_IP="$(docker inspect -f "{{ .NetworkSettings.Networks.bridge.IPAddress }}" aucar_rabbit)"
export BROKER_PORT=5672
export BROKER_VHOST=aucar
export BROKER_USER=aucar
export BROKER_PASS=aucar
```

```sh
docker run -d --name aucar_worker \
	-e BROKER_URL="pyamqp://${BROKER_PASS}:${BROKER_USER}@${BROKER_IP}:${BROKER_PORT}/${BROKER_VHOST}" \
	-e WEB_IP="localhost" \
	-e WEB_PORT="8000" \
	-v ${PWD}/../web/aucarvideo:/home/app/nfs \
	-p 8030:5555 \
	aucar_worker \
	/home/app/entrypoint.sh
```

* Celery Flower monitoring GUI port 5555
* You can access monitoring GUI by visiting http://container-ip:5555 in a browser or, if you need access outside the host, on port 8030.
* Or can then go to http://localhost:8030 or http://host-ip:8030 in a browser.

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

```sh
export BROKER_IP="ip-broker"
export BROKER_PORT=5672
export BROKER_VHOST=aucar
export BROKER_USER=aucar
export BROKER_PASS=aucar
```

```sh
docker run -d --name aucar_rabbit \
	-e BROKER_URL="pyamqp://${BROKER_PASS}:${BROKER_USER}@${BROKER_IP}:${BROKER_PORT}/${BROKER_VHOST}" \
	-e WEB_IP="ip-web" \
	-e WEB_PORT="port-web" \
	-v /etc/nfs:/home/app/nfs
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

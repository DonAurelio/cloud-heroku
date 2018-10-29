# Celery Worker Service

The cellery worker is resposible for processing the videos placed in the nfs folder by the WebService. 

## Requirements

1. Development: Linux OS (Local), Docker
2. Production: Centos OS (AWS), Docker, nfs-utils

## Run in Development

An place the **secrests.sh** file into worker directory to load the credentials into the container. Then run this command from the **worker directory**. .

```sh
docker run --name aucar_worker \
	-v ${PWD}/celery:/home/app/celery \
	-v ${PWD}/supervisor/conf.d:/etc/supervisor/conf.d \
	-v ${PWD}/supervisor/logs:/home/app/logs \
	-v ${PWD}/../web/aucarvideo/media:/home/app/nfs \
	aucar_worker
```

## Run in AWS

On this deployment the nfs folder is mounted on the AWS EC2 instance an shared with the container through a volume.

Configure AWS instance NFS

```sh
sudo yum install -y nfs-utils
```

Edit the /etc/hosts file of the WS instance and place at the end the private IPv4 Address of te FS service.

```sh
<ip_of_file_server_instance> 	nfs
```

Mount the FS shared directory and map that remote directory with the **media** folder on the web application.

```sh
sudo mkdir -p /etc/nfs
```

```sh
sudo mount -t nfs nfs:/etc/nfs /etc/nfs
```

Edit the /etc/fstab and add the line below to mount the FS shared directory every time the instance starts up. 

```sh
nfs:/etc/nfs /etc/nfs	nfs	rw,sync,hard,intr	0	0
```

### Run the Worker in a Docker Container

Run the container that will use the env variables defined on the AWS instance

```sh
docker run --name aucar_worker \
	-v ${PWD}/celery:/home/app/celery \
	-v ${PWD}/supervisor/conf.d:/etc/supervisor/conf.d \
	-v ${PWD}/supervisor/logs:/home/app/logs \
	-v /etc/home/nfs:/home/app/nfs \
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


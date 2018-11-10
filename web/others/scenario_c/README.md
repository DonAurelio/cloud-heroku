# AucarVideo 

Aucarvideo is a SaaS application which use **Semi Isolated Tennancy Approach** by meas of django-tenant-schema module.

## Requirements

1. Development: Docker, python-virtualenv
3. Deployment: Centos OS (AWS EC2 instance), Docker, docker-compose, nfs-utils

## Content

Each folder constains details about how to run the whole application both development and production enviroments. For each environment you need to deploy, so refer to each folder to read develop or deploy the application:

Development (Local)

	1. Rabbitmq
	2. Postgres
	3. Web (aucarvideo)
	4. Worker

Deployment
	
	1. NFS
	2. Rabbitmq or other broker
	3. Web
	4. Worker


## Utilities

On development or deployment some configurations would need you to install docker and docker-compose. 

* Install Docker and docker-compose in Centos OS (AWS EC2 instance).

```sh
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

# References

[django-tenant-schema](https://django-tenant-schemas.readthedocs.io/en/latest/)

[django-bootstrap3](https://github.com/dyve/django-bootstrap3)

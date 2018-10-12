# AucarVideo 

Aucarvideo is a SaaS application which use **Semi Isolated Tennancy Approach** by meas of django-tenant-schema module.

## Requirements

1. Development: Docker, Install python-virtualenv
3. Production: Centos OS (AWS EC2 instance), Docker, docker-compose, nfs-utils

## Content

Each folder constains details about how to run the whole application both development and production enviroments. For each environment you need to deploy, so refer to each folder to read develop or deploy the application:

Development (Local)

	1. Rabbitmq
	2. Postgres
	3. Web (aucarvideo)
	4. Worker

Production
	
	1. NFS
	2. Rabbitmq
	3. Web
	4. Worker

# References

[django-tenant-schema](https://django-tenant-schemas.readthedocs.io/en/latest/)

[django-bootstrap3](https://github.com/dyve/django-bootstrap3)

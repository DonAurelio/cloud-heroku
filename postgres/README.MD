# Postgres Datbase Service

The NFS server will be available for the WebServers and Workers. So they will share a media path on whih videos will be uploaded by mean of the WebServer. Then those videos will be processed by the Workers.

## Requirements

1. Deployment: Docker

## Deployment

Deploy the nfs server as follows within a Docker container

```sh
docker run -d --name aucar_postgres \
	-e POSTGRES_DB=aucar \
	-e POSTGRES_USER=aucar \
	-e POSTGRES_PASSWORD=aucar \
	-p 8010:5432 \
	postgres
```

Acces the database with pgadmin or other tool:

* Using the conainer container-ip:5432
* Using the host host-ip:8010 or localhost:8010. 


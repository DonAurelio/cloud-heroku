# Postgres Datbase Service

The NFS server will be available for the WebServers and Workers. So they will share a media path on whih videos will be uploaded by mean of the WebServer. Then those videos will be processed by the Workers.

## Requirements

1. Development: docker.io
2. Production: docker.io

## Run in Development

Deploy the nfs server as follows within a Docker container

```sh
docker run -d --name aucar_postgres \
	-e POSTGRES_DB=aucar \
	-e POSTGRES_USER=aucar \
	-e POSTGRES_PASSWORD=aucar \
	postgres
```
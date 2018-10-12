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
	-p 8010:5432 \
	postgres
```

* You can access database data with pgadmin by visiting container-ip:5432 or, if you need access outside the host, on port 8010, using host-ip:8010.
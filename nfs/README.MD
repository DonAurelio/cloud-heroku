# NFS Service

The NFS server will be available for the WebServers and Workers. So they will share a media path on whih videos will be uploaded by mean of the WebServer. Then those videos will be processed by the Workers.

## Requirements

1. Development: Docker
2. Deployment: Centos OS (AWS EC2 Instance), Docker

## Run in Development

Deploy the nfs server as follows within a Docker container

```sh
docker run -d --name aucar_nfs --privileged cpuguy83/nfs-server /etc/nfs/
```

## Deployment in AWS

The NFS Server will be setting up on bare metal in a AWS EC2 instance.

```sh
sudo yum install -y nfs-utils
```

Create the directory that will be shared over the network.

```sh
sudo mkdir -p /etc/nfs/
```

```sh
sudo nano  /etc/exports
```

Place the following on /etc/exports file. Note that * is not convenient for security since any machine can mount the folder. To provide security change * by the IP Addresses of the machines that are allowed to mount this directory. 

```sh
/etc/nfs/ *(rw,sync,no_root_squash)
```

```sh
exports -a
```

```sh
service nfs start
```

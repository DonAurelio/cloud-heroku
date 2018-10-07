# NFS Service

The NFS server will be available for the WebServers and Workers. So they will share a media path on whih videos will be uploaded by mean of the WebServer. Then those videos will be processed by 
celery workers. 

To run the nfs service you need to get Docker installed on your system.

```sh
docker run -d --name cloud_nfs --privileged cpuguy83/nfs-server /etc/nfs/media
```

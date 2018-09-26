# AucarVideo 

Aucarvideo is a SaaS application on which an organization (tenant) is registered on the application. For each organization registered a site is created (tenant) to keep the information of the organization separetely.

We use the **Semi Isolated Tennancy Approach** by meas of django-tenant-schema module. Semi Isolated Approach: Shared Database, Separate Schemas. One database for all tenants, but one schema per tenant.

## Requirements

Requirements for development

```sh
sudo apt-get update
```

```sh
sudo apt-get install docker.io
```

```sh
sudo groupadd docker
```

```sh
sudo usermod -aG docker $USER
```

```sh
sudo reboot now
```

```sh
sudo apt-get install python-pip
```

```sh
sudo pip install virtualenv
```

Additional requirements for production

```sh
sudo pip install docker-compose
```

## Setting Up the Development Environment

Create the development database using Docker. **Note: The data base container is created only the first time, to run the database in subsequent situations use 'docker start aucarvideo_db'.**

```sh
docker run --name aucarvideo_db -e POSTGRES_PASSWORD=aucarvideo -e POSTGRES_DB=aucarvideo -e POSTGRES_USER=aucarvideo -d postgres
```

Check the database is running in the container

```sh
sudo docker ps
```

the output should look as follows:

```sh
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
54504cdafc1d        postgres            "docker-entrypoint.s…"   48 seconds ago      Up 41 seconds       5432/tcp            aucarvideo_db
```

Verify the ip of the database server with the following command

```sh
docker inspect aucarvideo_db | grep IPAddress
```

the output should look as bellow, where **172.17.0.2** is the IP Address of the database server.

```sh
"SecondaryIPAddresses": null,
"IPAddress": "172.17.0.2",
        "IPAddress": "172.17.0.2",
```

Please place that IP Address on the **secrets.sh** file needed to run the project. **IMPORTANT: THIS PROJECT DOES NOT HAVE THE secrets.sh file SO YOU NEED TO ASK FOR IT TO THE ADMIN OF THIS PROJECT. THE SECRECTS FILE CONTAIN CONFIGURATION INFORMATION NEEDED FOR THE PROJECT TO RUN PROPERLY SUCH US DATABASE PASSWORDS, THE PROJECT SECURITY KEY, EMAIL USERNAME AND PASSWD, ETC.** 

```sh
sudo nano secrects.sh
```

Modify the **DB_HOST** variables for the IP Address of the database.

```sh
...

# For development change this to the IP 
# of the database service.
export DB_HOST="172.17.0.2"

...
```

Load the secrects into the system env variables.

```sh
source secrets.sh
```


Create the python virtualenvironment in the **aucarvideo** folder.

```sh
virtualenv --python=python3.6 .env
```

Verify the **.env** folder was created. **Note: the virtual env is created only the first time you going to develop in the application.** 

```sh
ll
```

the output should look as follows:

```sh
drwxr-xr-x 12 some some 4096 ago 28 21:30 ./
drwxr-xr-x  7 some some 4096 sep  2 19:08 ../
drwxr-xr-x  3 some some 4096 ago 26 22:58 aucarvideo/
drwxr-xr-x  5 some some 4096 sep  2 18:47 auth_tenants/
drwxr-xr-x  5 some some 4096 sep  2 18:47 contests/
drwxr-xr-x  6 some some 4096 sep  2 10:44 customers/
-rw-rw-r--  1 some some 1024 sep  2 16:46 Dockerfile
-rw-rw-r--  1 some some   84 sep  2 12:13 .dockerignore
-rwxrwxr-x  1 some some  534 sep  2 18:46 entrypoint.sh*
drwxr-xr-x  6 some some 4096 ago 28 06:14 .env/
drwxr-xr-x  4 some some 4096 sep  2 18:47 home_public/
drwxr-xr-x  3 some some 4096 sep  2 18:48 home_tenants/
-rwxr-xr-x  1 some some  542 ago 19 18:52 manage.py*
drwxrwxr-x  3 some some 4096 ago 27 17:07 media/
-rw-rw-r--  1 some some  131 ago 28 21:40 req_dev.txt
-rw-rw-r--  1 some some  134 ago 28 22:30 req_prod.txt
-rwxrwxr-x  1 some some  616 sep  2 20:44 secrets.sh*
drwxr-xr-x  3 some some 4096 ago 21 22:10 static/
drwxrwxr-x  2 some some 4096 ago 27 10:47 templates/
```

Activate the Python virtualenv. **Note: Every time you going to run the application for development you need to activate the virtualenv.** 

```sh
source .env/bin/activate
```

the prompt should change as shown bellow

```sh
some@host:~/Desktop/Grupo3/aucarvideo$
(.env) some@host:~/Desktop/Grupo3/aucarvideo$
```

Install requirements of the project.

```sh
pip3.6 install -r req_dev.txt
```

Run the migrations

```sh
./manage.py makemigrations
```

Apply migration changes to the database

```sh
./manage.py migrate_schemas
```

Apply tenants apps migrations changes to the database

```sh
./manage.py migrate_schemas --shared
```

Created the public tenant

```sh
./manage.py create_public_tenant
```

To run the project

```sh
./manage.py runserver 0.0.0.0:8000
```

Edit the /etc/hosts and add the name of the public tenant URL

```sh
sudo nano /etc/hosts
```

For every tenant you create you have to add it to the **/etc/hosts** file, so your
computer works as ad DNS server to translate the name **aucarvideo.com** to the 
local host IP address.

```sh
127.0.0.1	aucarvideo.com
127.0.0.1	facebook.aucarvideo.com
127.0.0.1	whatsapp.aucarvideo.com
...
```

Enter to the public web site http://aucarvideo.com:8000/.

## For Production in a Local Machine

**IMPORTANT: THIS PROJECT DOES NOT HAVE THE secrets.sh file SO YOU NEED TO ASK FOR IT TO THE ADMIN OF THIS PROJECT. THE SECRECTS FILE CONTAIN CONFIGURATION INFORMATION NEEDED FOR THE PROJECT TO RUN PROPERLY SUCH US DATABASE PASSWORDS, THE PROJECT SECURITY KEY, EMAIL USERNAME AND PASSWD, ETC.**

Before run the project, **place the secrets.sh file on the aucarvideo directory**. Then you can run the application and docker-compose will configure it automatically.


```sh
docker-compose up -d postgres
```

```sh
docker-compose up -d web
```

```sh
docker-compose up -d nginx
```

```sh
docker-compose up -d cron
```

Enter to the public web site http://aucarvideo.com/. Note: with -d flag services run as daemon processed, i.e., if your reboot your computer the services will start automatically.

To shuot down all services run the following command:

```sh
docker-compose down
```

If you perform some change in the service some times you need to rebbot it.

```sh
docker-compose restart <service_name>
```

Some settings require you rebuild the container again.

1. Stop the service

```sh
docker-compose stop <service_name>
```

2. Remove the service container

```sh
docker-compose rm <service_name>
```

3. Start the service again.

```sh
docker-compose rm <service_name>
```

## For Production in AWS

For this deployment three EC2 instances were considered: **WebServer (WS)**, **Worker (W)** and **FileServer (FS)**.

### Setting up the FileServer

The FS implements and NFS that will contains the media that is uploaded througth the WS. The W will mount the nfs media folder to get acces to the uploaded videos and perform its processing. As the processed videos will be put in to the **nfs media** folder the WS can see those processed videos and serve them.

```sh
sudo yum install -y nfs-utils
```

Create the directory that will be shared over the network.

```sh
sudo mkdir -p /home/ec2-user/nfs
```

```sh
sudo nano  /etc/exports
```

Place the following on /etc/exports file

```sh
/home/ec2-user/nfs *(rw,sync,no_root_squash)
```

```sh
exports -a
```

```sh
service nfs start
```
Install Git.

```sh
sudo yum install git
```

Clon this repository on the **nfs folder** instance.

```sh
cd /home/ec2-user/nfs/
```

```sh
git clone https://github.com/ISIS4426-Desarrollo-Soluciones-Cloud/Grupo03.git
```

**IMPORTANT: Check that every machine that will be moun th nfs folder is in the same AWS EC2 Security Group and that Security Group can communicate over the NFS. If this is not set. Service can't mount the NFS shared directory.**


### Setting up the WebServer

The WS have to mount the FS folder to place there the media content uploaded by users.

```sh
sudo yum install -y nfs-utils
```

Edit the /etc/hosts file of the WS instance and place at the end the private IPv4 Address of te FS service.

```sh
<ip_of_file_server_instance> 	nfs
```

Mount the FS shared directory and map that remote directory with the **media** folder on the web application.

```sh
sudo mount -t nfs nfs:/home/ec2-user/nfs /home/ec2-user/app
```

Edit the /etc/fstab and add the line below to mount the FS shared directory every time the instance starts up. 

```sh
nfs:/home/ec2-user/nfs	/home/ec2-user/app	nfs	rw,sync,hard,intr	0	0
```

Install Docker and docker-compose in the WS instance.

```sh
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Run the WS

```sh
docker-compose -f docker-compose-web.yml up -d web 
```

```sh
docker-compose -f docker-compose-web.yml up -d nginx 
```

### Setting up the Worker

The W have to mount the FS folder to be able to process the videos placed in the media remote directory.

```sh
sudo yum install -y nfs-utils
```

Edit the /etc/hosts file of the WS instance and place at the end the private IPv4 Address of te FS service.

```sh
<ip_of_file_server_instance> 	nfs
```

Mount the FS shared directory and map that remote directory with the **media** folder on the web application.

```sh
sudo mount -t nfs nfs:/home/ec2-user/nfs /home/ec2-user/app
```

Edit the /etc/fstab and add the line below to mount the FS shared directory every time the instance starts up. 

```sh
nfs:/home/ec2-user/nfs	/home/ec2-user/app	nfs	rw,sync,hard,intr	0	0
```

Install Docker and docker-compose in the WS instance.

```sh
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Run the WS

```sh
docker-compose up -d cron -f docker-compose-cron.yml
```

# References

[django-tenant-schema](https://django-tenant-schemas.readthedocs.io/en/latest/)

[django-bootstrap3](https://github.com/dyve/django-bootstrap3)


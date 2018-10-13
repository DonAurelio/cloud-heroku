# AucarVideo 

Aucarvideo is a SaaS application which use **Semi Isolated Tennancy Approach** by meas of django-tenant-schema module.

## Requirements

1. Development: Docker, python-virtualenv, docker-compose
2. Production: Centos OS (AWS EC2 Instance) Docker, docker-compose

## Run in Development

**IMPORTANT:** Request the admin of this repo for the **secrects.sh** file needed to run this application and place it on aucarvideo folder. **Check the development vaiables are properly configured**.


```sh
cat aucarvideo/secrets.sh
```

Get into the aucarvideo folder

```sh
cd aucarvideo/
```

Load the secrects into the system env variables.

```sh
source secrets.sh
```

Create the python virtualenvironment in the **aucarvideo** folder.

```sh
virtualenv --python=python3.6 .env
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
pip3.6 install -r requirements.txt
```

Run the migrations

```sh
python3.6 manage.py makemigrations
```

Apply migration changes to the database

```sh
python3.6 manage.py migrate_schemas
```

Apply tenants apps migrations changes to the database

```sh
python3.6 manage.py migrate_schemas --shared
```

Created the public tenant

```sh
python3.6 manage.py create_public_tenant
```

Run the project

```sh
python3.6 manage.py runserver 0.0.0.0:8000
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

## Run in AWS



<!-- ## For Production in a Local Machine

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

**IMPORTANT: Check that every machine that will be moun th nfs folder is in the same AWS EC2 Security Group and that Security Group can communicate over the NFS. If this is not set. Service can't mount the NFS shared directory.**


### Setting up the WebServer

The WS have to mount the FS folder to place there the media content uploaded by users.

Install Git.

```sh
sudo yum install git
```

Clon this repository on the **nfs folder** instance.

```sh
git clone https://github.com/ISIS4426-Desarrollo-Soluciones-Cloud/Grupo03.git
```

```sh
sudo yum install -y nfs-utils
```

Edit the /etc/hosts file of the WS instance and place at the end the private IPv4 Address of te FS service.

```sh
<ip_of_file_server_instance> 	nfs
```

Mount the FS shared directory and map that remote directory with the **media** folder on the web application.

```sh
sudo mount -t nfs nfs:/home/ec2-user/nfs /home/ec2-user/Grupo03/aucarvideo/media
```

Edit the /etc/fstab and add the line below to mount the FS shared directory every time the instance starts up. 

```sh
nfs:/home/ec2-user/nfs	/home/ec2-user/Grupo03/aucarvideo/media	nfs	rw,sync,hard,intr	0	0
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
cd /home/ec2-user/Grupo03/aucarvideo
```

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
sudo mount -t nfs nfs:/home/ec2-user/nfs /home/ec2-user/Grupo03/cron/media
```

Edit the /etc/fstab and add the line below to mount the FS shared directory every time the instance starts up. 

```sh
nfs:/home/ec2-user/nfs	/home/ec2-user/Grupo03/cron/media/	nfs	rw,sync,hard,intr	0	0
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
docker-compose -f docker-compose-cron.yml up -d cron 
``` -->

# References

[django-tenant-schema](https://django-tenant-schemas.readthedocs.io/en/latest/)

[django-bootstrap3](https://github.com/dyve/django-bootstrap3)



<!-- python3.6 cron/script.py ${PWD}/aucarvideo/ localhost 8000 ${PWD}/cron/time.log -->
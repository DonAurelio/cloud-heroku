# AucarVideo 

Aucarvideo is a SaaS application which use **Semi Isolated Tennancy Approach** by meas of django-tenant-schema module.

## Requirements

1. Development: Docker, python-virtualenv, docker-compose
2. Production: Centos OS (AWS EC2 Instance), Docker, docker-compose

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

## Deployment in AWS

Install Git.

```sh
sudo yum install git
```

Clone this repository on the Web instance.

```sh
git clone https://github.com/ISIS4426-Desarrollo-Soluciones-Cloud/Grupo03.git
```

Install nfs-utils 

```sh
sudo yum install -y nfs-utils
```

Edit the /etc/hosts file of the WS instance and place at the end the private IPv4 Address of te FS service.

```sh
<ip_of_nfs_server_instance> 	nfs
```

Mount the NFS shared directory (the nfs server must be running, and in the same AWS region of web instance)

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

Place into the web directory and perform

```sh
docker-compose up -d
```

# References

[django-tenant-schema](https://django-tenant-schemas.readthedocs.io/en/latest/)

[django-bootstrap3](https://github.com/dyve/django-bootstrap3)


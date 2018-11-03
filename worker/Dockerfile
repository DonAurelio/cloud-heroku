# Base image
FROM python:3.6

# Image propietary
LABEL maintainer="Aurelio Vivas <aa.vivas@uniandes.edu.co>"

# Update the index of available packages
RUN apt-get update

# Install the ffmpeg package to video convertion
# Supervisor to run non demonized programs in background
RUN apt-get install -y ffmpeg supervisor

# Directory on which the application will reside
RUN mkdir -p /home/app

# Working directory inside the container
WORKDIR /home/app

COPY ./requirements.txt .
COPY ./entrypoint.sh .

# Directory to mount the remote nfs folder
RUN mkdir -p /home/app/nfs

# Directory to keep supervisor logs
RUN mkdir -p /home/app/logs

# Installing requirements
RUN pip3.6 install --no-cache-dir -r requirements.txt

# Flower port
EXPOSE 5555

# Contaner startup script
ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]


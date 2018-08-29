# Base image
FROM python:3.6

# Image propietary
LABEL maintainer="Aurelio Vivas <aa.vivas@uniandes.edu.co>"

ENV PYTHONUNBUFFERED 1

# Working directory inside the container
WORKDIR /usr/src/app

# Copy the project into the container current workdir
COPY . .

RUN apt-get update -y

RUN apt-get install -y libpq-dev python3-dev

# Installing requirements
RUN pip3.6 install --no-cache-dir -r req_prod.txt

# ENV SECRET_KEY '0p6cu%4z8!=tlrhl#ssy8ox)$#aaq8n4x%wu9g0xcd-w$01&9+'

# Informs Docker that the container listens on the specified network ports at runtime
# The EXPOSE instruction does not actually publish the port. It functions as a type of 
# documentation between the person who builds the image and the person who runs the container, 
# about which ports are intended to be published. To actually publish the port when running 
# the container, use the -p flag on docker run to publish and map one or more ports, or the -P 
# flag to publish all exposed ports and map them to to high-order ports.
EXPOSE 80
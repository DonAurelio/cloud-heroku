# Base image
FROM python:3.6-alpine

# Image propietary
LABEL maintainer="Aurelio Vivas <aa.vivas@uniandes.edu.co>"

# Update the index of available packages
RUN apk update

# Install the ffmpeg package to video convertion
RUN apk install ffmpeg

# Working directory inside the container
WORKDIR /usr/src/app

# Copy the project into the container current workdir
COPY . .

# Installing requirements
RUN pip3.6 install --no-cache-dir -r requirements.txt



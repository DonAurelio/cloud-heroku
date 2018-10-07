# Base image
FROM python:3.6

# Image propietary
LABEL maintainer="Aurelio Vivas <aa.vivas@uniandes.edu.co>"

# Update the index of available packages
RUN apt-get update

# Install the ffmpeg package to video convertion
RUN apt-get install -y ffmpeg

# Working directory inside the container
WORKDIR /home/app

# Copy the project into the container current workdir
COPY . .

# Installing requirements
RUN pip3.6 install --no-cache-dir -r requirements.txt

FROM python:3.9-slim-buster

# set our working directory inside the container (when it's finally created from this image)
# depending on your environment you may need to
# RUN mkdir -p /app
WORKDIR /app

# depending on your environment you may also need to
RUN mkdir -p /postgres_data

# set environment variables
# Prevents Python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update \
   && apt-get -y install netcat gcc postgresql \
   && apt-get clean

# Setup GDAL
RUN apt-get update &&\
   apt-get install -y binutils libproj-dev gdal-bin python-gdal python3-gdal

# upgrade pip version
RUN pip install --upgrade pip

# copy requirements to the image
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

# Copy over the project
COPY . /app
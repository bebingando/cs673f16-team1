# Create application container
# when container is run, http://localhost should be accessible from web browser

# start with prereqs v0.0.1
FROM cs673/team_alpha_project_prereqs:latest

MAINTAINER Anthony Valencia anthonysvalencia@gmail.com

ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST "redis"

RUN mkdir /home/g1

RUN mkdir /home/g1/database

RUN mkdir /home/g1/source

RUN mkdir /home/g1/source/group1

RUN mkdir /home/g1/virtualenv

RUN mkdir /home/g1/static

# COPY source code into container home directory
COPY ./resources/group1/ /home/g1/source/group1/

RUN ls /home/g1/source/group1/

# set working directory
WORKDIR /home/g1/source/group1/

# make migration files
RUN python manage.py makemigrations

# run database migration
RUN python manage.py migrate

# run database population
RUN python manage.py populate_demo_data --issues 50 --projects 5

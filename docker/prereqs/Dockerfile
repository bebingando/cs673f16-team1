# Creates a prereqs container

# start with ubuntu v14.04
FROM ubuntu:14.04

MAINTAINER Anthony Valencia anthonysvalencia@gmail.com

# update aptitude with new repo
RUN apt-get update

# install python development libraries
RUN apt-get -y install python-pip python-dev

# readline dependencies
RUN apt-get -y install libncurses5-dev
RUN apt-get -y install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

# install boto3
ADD dependencies.txt /
RUN pip install -r dependencies.txt



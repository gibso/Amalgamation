# use ubuntu image because hets can only be installed from ppa in ubuntu
FROM ubuntu:18.04

# install hets
RUN apt-get update
RUN apt-get install -y software-properties-common libmysqlclient20
RUN dpkg --add-architecture i386
RUN apt-add-repository ppa:hets/hets
RUN apt-get update
RUN apt-get install -y hets-desktop

# install python and lua
RUN apt-get install -y python2.7 python2.7-dev lua5.1 lua5.1-policy-dev

# add workdir for mounting the project
RUN mkdir /opt/project
WORKDIR /opt/project

# for this entrypoint, you have to mount the project folder into /opt/project
CMD ["/usr/bin/python2.7", "run-blending.py"]
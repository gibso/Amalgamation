FROM python:latest

# add workdir for mounting the project
RUN mkdir /opt/project
WORKDIR /opt/project

# copy requirements file and install python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# for this entrypoint, you have to mount the project folder into /opt/project
CMD ["python", "run-blending.py"]
FROM continuumio/anaconda3:latest

# install patassco clingo
RUN conda install --yes --channel potassco clingo

# add workdir for mounting the project
RUN mkdir /opt/project
WORKDIR /opt/project

# copy requirements file and install python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# start the blending process
CMD ["python", "run-blending.py"]
FROM continuumio/anaconda3:latest

# install patassco clingo
RUN conda install --yes --channel potassco clingo

# add workdir for mounting the project
RUN mkdir /opt/project
WORKDIR /opt/project

# copy everything
COPY . .

# install dependencies
RUN  pip install -e .

# start flask server
CMD flask run --host=0.0.0.0

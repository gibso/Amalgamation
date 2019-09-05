FROM continuumio/anaconda3:2019.07

# install patassco clingo
RUN /opt/conda/bin/conda install --yes --channel potassco clingo

# add workdir for mounting the project
RUN mkdir /opt/project
WORKDIR /opt/project

# copy everything
COPY . .

# install dependencies
RUN /opt/conda/bin/pip install -e .

# start flask server
CMD /opt/conda/bin/flask run --host=0.0.0.0

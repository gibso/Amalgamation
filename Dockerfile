FROM spechub2/hets:latest

# install dependencies for anaconda
RUN apt-get update && apt-get install -y libgl1-mesa-glx \
 libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 \
 libxcomposite1 libasound2 libxi6 libxtst6 wget

# install anaconda3
WORKDIR /opt
RUN wget https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh
RUN bash Anaconda3-2019.07-Linux-x86_64.sh -b -p /opt/conda

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

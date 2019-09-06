COINVENT Amalgamation Module 									
=================================

This project is a fork of the [original Amalgamation Module by Manfred Eppe](https://github.com/meppe/Amalgamation) and is part of the [Orpheus Application](https://github.com/gibso/orpheus-dev).

### Overview
In this fork, the amalgamation module is embedded into a flask server, and can be executed by an API call.
Furthermore, the HETS dependency has been encapsulated into another project, called [hets-api](https://github.com/gibso/hets-api).

This is the amalgamation system which is the core of the blending process. The current state (22.04.15) should run with some music examples and the example of blending the theory of naturals with the theory of lists to obtain some novel lemma for the theory of lists. 
It currently works with CASL only, and relies on HETS (via commandline-call) to compute colimits. In future versions it will rely also on language modules to have language-independence, and HDTP to improve generalization search. 

### Endpoint
when running the server e.g. on http://localhost:5000, you can request the following endpoint:

##### POST  http://localhost:5000/amalgamation

The endpoint expects a .casl file, that contains algebraic specification of the input spaces. Make sure to place it as a `multipart/form-data` object under a key called `file`. Furthermore, you need to pass the explicit name of the input spaces as form data, under a key called `input-space-names` e.g.
```
file: (binary)
input-space-names: ["G7","Bbmin"]
```
 
 If you have trouble with that, take a look at the [test file](https://github.com/gibso/Amalgamation/blob/master/tests/amalgamation_test.py).

### Setup using [docker](https://www.docker.com/get-started)

I highly recommend to use [docker](https://www.docker.com/get-started) for running this project. Clone this project by running 
```
git clone https://github.com/gibso/Amalgamation
```
and enter the directory: `cd Amalgamation`

Build a docker image of the project by running
```
docker build -t amalgamation .
```

When starting the flask server in a docker container, you need to pass an instance of the [hets-api](https://github.com/gibso/hets-api) host as environment variable. Furthermore, the hets-api and the amalgamation server need to share the same /data folder, by mounting it. If hets-api is running at localhost:5000, start the amalgamation server with
```
docker run --rm -it -p 4000:5000 -e "HETSAPI_HOST=localhost:5000" -v ~/data:/data amalgamation
```

Now you can reach your amalgamation server at http://localhost:4000.

### Authors:
- Manfred Eppe (meppe@iiia.csic.es)
- Roberto Confalonieri (confalonieri@iiia.csic.es)
- Ewen MacLean (ewenmaclean@gmail.com)
- Oliver Görtz (oliver.goertz{at}gmail.com)

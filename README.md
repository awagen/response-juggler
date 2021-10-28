What is the project about
=========================
The project provides a simple response faker based on given sampling criteria as defined below.
It builds on FastAPI.
Main use right now is json response sampling to mock services for testing purposes.

Start the app
=============
- https://fastapi.tiangolo.com/tutorial/first-steps/
- Arguments:
    - main: file main.py
    - app: the object created inside of main.py with the line app = FastAPI()
    - --reload:  make the server restart after code changes. Only use for development.
    - to start app, cd into main project folder (one level before src) and run:
```shell script
uvicorn main:app --reload  --env-file ./files/local-env.env --loop asyncio
```
Configuring loop to utilize asyncio is required to do utilization of the hack
of nested_asyncio, which effectively allows multiple executions chiming in on
one loop (uvicorn already starts one up and without the hack utilizing it for
executions in our logic wouldnt work due to "loop already running")

- build docker img (project root): ```docker build -t response-juggler .```

- run: 
    -```docker run --env-file ./files/local-env.env -d -p 80:80 response-juggler```

Definition of response sampling
===============================
The sampling of each response takes the main template as basis.
Within this template, further partials (another json) or fields can be referenced
for sampling by placing a placeholder and making sure within the configuration
env variables, in case of partial each used partial is defined properly with below
settings (RESPONSE_PARTIAL_ setting prefix below), where settings belonging to single partial have to use the same PARTIAL_NAME placeholder below.
The same holds for fields (RESPONSE_FIELD_ setting prefix below), where fields dont refer to other jsons to sample and fill in,
but to actual values, so placeholders corresponding to fields can exist in
the main template or in partials.

The definition of the response consists of the following parts:
- ```RESPONSE_MAIN_TEMPLATE```: the main json container of the response, path relative to src/templates folder
- ```RESPONSE_PARTIAL_IDENT_[PARTIAL_NAME]```: value of the placeholder used in the content of the partial for the respective partial name
(name can be any, just needs to be consistent across settings for a single partial)
- ```RESPONSE_PARTIAL_CONTENT_[PARTIAL_NAME]```: the file defining the partial content, path relative to src/templates/partials folder
- ```RESPONSE_PARTIAL_SAMPLER_TYPE_[PARTIAL_NAME]```: the sampler type, for partials can only be SINGLE or LIST
- ```RESPONSE_PARTIAL_SAMPLER_MIN_NUM__[PARTIAL_NAME]```: in case of sampler type LIST, defines the minimal nr of samples
- ```RESPONSE_PARTIAL_SAMPLER_MAX_NUM__[PARTIAL_NAME]```: in case of sampler type LIST, defines the maximal nr of samples
- ```RESPONSE_FIELD_IDENT_[FIELD_NAME]```: the placeholder of the field in partial or main template to replace
- ```RESPONSE_FIELD_SAMPLER_TYPE_[FIELD_NAME]```: type of sampling, possible values SINGLE or LIST
- ```RESPONSE_FIELD_SAMPLER_REPEAT_[FIELD_NAME]```: in case of LIST sampling, defines whether single elements can be repeated in the sampling (with / without replacement). true/false. 
- ```RESPONSE_FIELD_SAMPLER_ELEMENT_CAST_[FIELD_NAME]```: defines which type the comma-separated selection options shall be cast to (available: INT, FLOAT, BOOL, STRING)
- ```RESPONSE_FIELD_SAMPLER_SELECTION_[FIELD_NAME]```: comma separated list of possible values to sample from
- ```RESPONSE_FIELD_SAMPLER_MIN_NUM_[FIELD_NAME]```: in case of LIST sampling, defines minimal number of samples
- ```RESPONSE_FIELD_SAMPLER_MAX_NUM_[FIELD_NAME]```: in case of LIST sampling, defines maximal number of samples
  
Overview of endpoints
=====================

- ```[host]:[port]/```: simple hello response
- ```[host]:[port]/search```: returns the sampling output defined by env variables,
response differs between calls due to the random sampling

FastAPI comes with swagger endpoint on /docs (e.g localhost:80/docs)


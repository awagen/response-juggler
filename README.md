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
  
Overview of endpoints
=====================
FastAPI comes with swagger endpoint on /docs (e.g localhost:80/docs)


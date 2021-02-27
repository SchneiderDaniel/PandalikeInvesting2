# PandalikeInvesting2 Website
This is the code of my new homepage.
It is based on:
[Gentelella](https://github.com/puikinsh/gentelella) is a free to use Bootstrap admin template.

## Installation


You should create a virtual environment and install the required packages with the following commands:

    windows:
    python -m venv env
    .\env\Scripts\activate    
    (env) $ pip install -r requirements.txt


    Linux:
    python3 -m venv env
    source env/bin/activate
    (env) $ pip install -r requirements.txt

## Run


In order to run it make sure that your venv is runnig and then

    Windows:
    $ .\env\Scripts\activate 
    (env) $ env:FLASK_APP="run.py"
    (env) $ flask run

    Linux:
    source env/bin/activate
    (env) $ env:FLASK_APP="run.py"
    (env) $ flask run


or

    Windows:
    $ .\env\Scripts\activate 
    (env) $ pyhton run.py

    Linux:
    source env/bin/activate
    (env) $ pyhton run.py



## Setup your env variables
You need to set the following env. variables.

    RECAPTCHA_PUBLIC_KEY
    RECAPTCHA_PRIVATE_KEY
    SECRET_KEY
    DATABASE_URI (example: sqlite:///site.db)
    ADMIN_USER
    ADMIN_EMAIL
    ADMIN_PASSWORD
    CONFIG_MODE (Debug/Production)
 

## Docu
[Flask Security](https://flask-security-too.readthedocs.io/en/stable/)
[Dash](https://dash.plotly.com/)




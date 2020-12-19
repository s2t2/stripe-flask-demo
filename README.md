# My Flask App (Template)

## Setup

Create and activate a virtual environment, perhaps named "my-flask-env" or something:

```sh
conda create -n my-flask-env python=3.8 # first time only
conda activate my-flask-env
```

Install package dependencies inside the virtual environment:

```sh
pip install -r requirements.txt
```

## Usage

Run the app (then view in browser at localhost:5000):

```sh
FLASK_APP=web_app flask run
```

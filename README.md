# Stripe Payment Page Demo (Flask)

An example payment processing page, using the Stripe API. Adapted from the [docs example](https://stripe.com/docs/checkout/integration-builder).


## Setup

Create and activate a virtual environment, perhaps named "stripe-flask-env" or something:

```sh
conda create -n stripe-flask-env python=3.8 # first time only
conda activate stripe-flask-env
```

Install package dependencies inside the virtual environment:

```sh
pip install -r requirements.txt # first time only
```

Configure environment variables, including [Stripe API Key](https://dashboard.stripe.com/test/apikeys):

```sh
# .env file contents

STRIPE_PUBLIC_KEY="pk_test_______________"
STRIPE_SECRET_KEY="sk_test_______________"
```

## Usage

Run the app (then view in browser at localhost:5000):

```sh
FLASK_APP=web_app flask run
```

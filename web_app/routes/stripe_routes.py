
import os
from dotenv import load_dotenv
from flask import Blueprint, render_template, flash, redirect, jsonify, request
import stripe

stripe_routes = Blueprint("stripe_routes", __name__)

load_dotenv()

APP_DOMAIN = os.getenv("APP_DOMAIN", default="http://localhost:5000")
SUCCESS_URL = f"{APP_DOMAIN}/stripe/checkout-session/callback/success" # must match route defined below
CANCEL_URL = f"{APP_DOMAIN}/stripe/checkout-session/callback/cancel" # must match route defined below

STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY", default="PK_OOPS") # client-side
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", default="SK_OOPS") # server-side

stripe.api_key = STRIPE_SECRET_KEY

@stripe_routes.route("/stripe/checkout-session/new")
def checkout_page():
    print("CHECKOUT PAGE")
    EXAMPLE_PRODUCT = {
        "name": "My Book",
        "price_usd": "$129.00",
        "img":{"url": "https://i.imgur.com/EHyR2nP.png", "alt": "The cover of my book"}
    } # todo: fetch product(s) from stripe
    return render_template("stripe_checkout.html", stripe_pk=STRIPE_PUBLIC_KEY, product=EXAMPLE_PRODUCT)

@stripe_routes.route("/stripe/checkout-session/create", methods=["POST"])
def create_checkout_session():
    """Launches a new stripe payment page with product info and credit card form """
    print("CREATE CHECKOUT")
    #print("FORM DATA:", dict(request.form))
    #products = dict(request.form)

    line_items = [
        {
            "price_data": {
                "currency": "usd",
                "unit_amount": 129_00,
                "product_data": {"name": "My Book", "images": ["https://i.imgur.com/EHyR2nP.png"]},
            },
            "quantity": 1
        }
    ] # todo: pass selected products from the form data

    try:
        checkout_session = stripe.checkout.Session.create(
            success_url=SUCCESS_URL,
            cancel_url=CANCEL_URL,
            mode="payment",
            payment_method_types=["card"],
            line_items=line_items,
            #client_reference_id="", # A unique string to reference the Checkout Session. This can be a customer ID, a cart ID, or similar, and can be used to reconcile the session with your internal systems.
            #customer_email="hello@example.com", # If provided, this value will be used when the Customer object is created. If not provided, customers will be asked to enter their email address.
            #discount=[{"type": "coupon", "___": "____"}]
            #submit_type="book", # "auto", "pay", "book", "donate"
        )
        return jsonify({"id": checkout_session.id})
    except Exception as e:
        print("ERR:", e)
        return jsonify(error=str(e)), 403

@stripe_routes.route("/stripe/checkout-session/callback/success")
def callback_success():
    """Triggers after the user successfully enters their card info on the checkout page """
    print("CHECKOUT SUCCESS")
    flash("Payment Received. Thanks!", "success")
    return redirect("/")

@stripe_routes.route("/stripe/checkout-session/callback/cancel")
def callback_cancel():
    """Triggers if the user gets to the stripe checkout and then presses the back button there (not the browser back button) """
    print("CHECKOUT CANCELED")
    flash("Payment Canceled. Are you sure?", "warning")
    return redirect("/")

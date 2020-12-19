
import os
from dotenv import load_dotenv
from flask import Blueprint, render_template, flash, redirect, jsonify, request
import stripe

load_dotenv()

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", default="OOPS")
stripe.api_key = STRIPE_SECRET_KEY

APP_DOMAIN = os.getenv("APP_DOMAIN", default="http://localhost:5000")
SUCCESS_URL = f"{APP_DOMAIN}/stripe/callback/success.html"
CANCEL_URL = f"{APP_DOMAIN}/stripe/callback/cancel.html"

LINE_ITEMS = [
    {
        "price_data": {
            "currency": "usd",
            "unit_amount": 2_99,
            "product_data": {"name": "Stubborn Attachments", "images": ["https://i.imgur.com/EHyR2nP.png"]},
        },
        "quantity": 1
    }
]

stripe_routes = Blueprint("stripe_routes", __name__)

@stripe_routes.route("/stripe/checkout")
def checkout_page():
    return render_template("stripe_checkout.html")

@stripe_routes.route("/stripe/create-checkout-session", methods=["POST"])
def create_checkout_session():
    print("CREATE CHECKOUT SESSION...")

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=LINE_ITEMS,
            mode="payment",
            success_url=SUCCESS_URL,
            cancel_url=CANCEL_URL,
        )
        return jsonify({"id": checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403

@stripe_routes.route("/stripe/callback/success")
def callback_success():
    return "SUCCESS!"

@stripe_routes.route("/stripe/callback/cancel")
def callback_cancel():
    return "OOPS SOMETHING WENT WRONG!"

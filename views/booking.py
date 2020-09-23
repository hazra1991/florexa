from flask import Blueprint,request

booking = Blueprint(__name__)

@booking.route("/")
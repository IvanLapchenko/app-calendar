from flask import request, make_response, jsonify
from flask_login import current_user
from .communicate_with_db import add_item_to_db, get_events_for_current_user_by
from database import Event
from . import app


def make_response_with_headers(data, *headers):
    response = make_response(jsonify(data))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', *headers)
    response.headers.add('Access-Control-Allow-Headers', '*')
    return response


@app.route("/create_event", methods=["POST"])
def create_event():
    data_from_request = request.get_json()
    data_from_request["user"] = "admin"
    event = Event(**data_from_request)
    add_item_to_db(event)
    response = make_response()
    response.status_code = 200
    return response


@app.route("/get_events_by/<date>", methods=["GET"])
def get_events_by(date):
    data = get_events_for_current_user_by(date)
    response = make_response_with_headers(data, "GET")
    return response
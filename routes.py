from datetime import datetime
import json
from flask import request, make_response, jsonify
from .communicate_with_db import add_item_to_db, get_events_for_current_user_by
from .database import Event
from . import app


def change_format_of_data(data_to_format):
    request_str_data = data_to_format.decode('utf-8')
    jsonified_dict = json.loads(request_str_data)
    jsonified_dict["user"] = "admin"
    jsonified_dict["date"] = datetime.strptime(jsonified_dict["date"], "%Y-%m-%d").date()
    jsonified_dict["time"] = datetime.strptime(jsonified_dict["time"], "%H:%M").time()
    return jsonified_dict


def make_response_with_headers(data, *headers):
    response = make_response(jsonify(data))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', *headers)
    response.headers.add('Access-Control-Allow-Headers', '*')
    return response


@app.route("/create_event", methods=["POST"])
def create_event():
    request_byte_string = request.data
    data_from_request = change_format_of_data(request_byte_string)
    event = Event(**data_from_request)
    add_item_to_db(event)
    response = make_response_with_headers("success", "POST")
    response.status_code = 200
    return response


@app.route("/get_events_by/<date>", methods=["GET"])
def get_events_by(date):
    data = get_events_for_current_user_by(date)
    response = make_response_with_headers(data, "GET")
    return response
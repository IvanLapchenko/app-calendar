from datetime import datetime
import json
from flask import request, make_response, jsonify
from .communicate_with_db import add_item_to_db, get_events_for_current_user_by
from .database import Event
from . import app


def change_format_of_data(data_to_format):
    request_str_data = data_to_format.decode('utf-8')
    jsonified_dict = json.loads(request_str_data)
    jsonified_dict["user"] = 1
    jsonified_dict["date"] = 1
    jsonified_dict["time"] = 1
    return jsonified_dict


@app.route("/create_event", methods=["POST"])
def create_event():
    if request.data:
        print(type(request.data))
        request_byte_string = request.data
        jsonified_dict = json.loads(request_byte_string)
        print(request_byte_string)
        print(jsonified_dict)
    else:
        print(request.data)
    # event = Event(**data_from_request)
    # add_item_to_db(event)
    response = make_response("success")
    response.status_code = 200
    return response


@app.route("/get_events_by/<date>", methods=["GET"])
def get_events_by(date):
    date = "date"
    data = get_events_for_current_user_by(date)
    response = make_response(data)
    return response

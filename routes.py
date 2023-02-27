from datetime import datetime
import json
from flask import request, make_response
from .communicate_with_db import add_item_to_db, get_events_for_current_user_by
from .database import Event
from . import app


def convert_time_to_object(time_to_format):
    return datetime.strptime(time_to_format, "%H:%M").time()


def convert_date_to_object(date_to_format):
    return datetime.strptime(date_to_format, "%Y-%m-%d").date()


def prepare_data_to_database(data):
    data = json.loads(data)
    data["user"] = 1
    data["date"] = convert_date_to_object(data["date"])
    data["time"] = convert_time_to_object(data["time"])
    return data


@app.route("/create_event", methods=["POST"])
def create_event():
    if request.data:
        request_data = prepare_data_to_database(request.data)

        print(request_data)
        event = Event(**request_data)
        add_item_to_db(event)

        response = make_response("success")
        response.status_code = 200

        return response
    return make_response("there's no data", 400)


@app.route("/get_events_by/<date>", methods=["GET"])
def get_events_by(date):
    date = datetime.fromisoformat(date)
    data = get_events_for_current_user_by(date)
    response = make_response(data)
    return response

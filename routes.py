from werkzeug.security import check_password_hash
from .communicate_with_db import add_item_to_db, get_events_for_current_user_by, get_user_by_nickname
from flask import request, make_response
from datetime import datetime
from .database import Event
from . import app
import json
import jwt


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
    data = get_events_for_current_user_by(date, 1)
    response = make_response(data)
    return response


@app.route("/login", methods=["POST"])
def login():
    request_data = json.loads(request.data)
    user = get_user_by_nickname(request_data["nickname"])

    if user:
        is_password_correct = check_password_hash(user.password, request_data["password"])

        if is_password_correct:
            payload = {
                "user_id": user.id,
                "exp": None,
                "iat": datetime.utcnow()
            }

            token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")

            response = make_response({"isLogged": True, "token": token})
            response.status_code = 200
            return response

        response = make_response({"isLogged": False})
        response.status_code = 400
        return response

from werkzeug.security import check_password_hash, generate_password_hash
from .communicate_with_db import add_item_to_db, get_events_for_current_user_by, get_user_by_nickname
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask import request, make_response, jsonify
from datetime import datetime, timedelta
from .database import Event, User
from . import app
import json


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
@jwt_required()
def create_event():
    if request.data:
        request_data = prepare_data_to_database(request.data)

        print(request_data)
        event = Event(**request_data)
        add_item_to_db(event)

        response = make_response({"msg": "success"})
        response.status_code = 200

        return response
    return make_response({"msg": "there's no data"}, 400)


@app.route("/get_events_by/<date>", methods=["GET"])
@jwt_required()
def get_events_by(date):
    current_user = get_jwt_identity()
    print(current_user)
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
            token = create_access_token(identity=user.id, expires_delta=timedelta(days=30))

            response = make_response({"isLogged": True, "token": token})
            response.status_code = 200
            return response

        response = make_response({"isLogged": False})
        response.status_code = 400
        return response


@app.route("/signup", methods=["POST"])
def signup():
    request_data = json.loads(request.data)
    user = get_user_by_nickname(request_data["nickname"])

    if user:
        response = make_response({"isAddedToDB": False, "reason": "user exist"})
        response.status_code = 409
        return response

    password = generate_password_hash(request_data["password"])
    user = User(request_data["nickname"], request_data["email"], password)
    add_item_to_db(user)

    response = make_response({"isAddedToDB": True})
    response.status_code = 200
    return response

""" Defines functions to fetch and return data """

from math import ceil
import hashlib
import json

from settings import Config
from decorators import check_token
from data_provider_service import DataProviderService

from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for

db_engine = Config.DB_ENGINE
DATA_PROVIDER = DataProviderService(db_engine)

PAGE_SIZE = 2


def initialize_database():
    """ Initializes database """
    DATA_PROVIDER.init_database()


def fill_database():
    """ Seeds database """
    DATA_PROVIDER.fill_database()


def candidates(serialize=True):
    """ Returns candidates """

    candidates_list = DATA_PROVIDER.get_candidate(serialize=serialize)
    page = request.args.get("page")

    if page:
        number_of_pages = int(ceil(float(len(candidates_list)) / PAGE_SIZE))
        converted_page = int(page)
        if converted_page > number_of_pages or converted_page < 0:
            return make_response("", 404)

        from_index = converted_page * PAGE_SIZE - PAGE_SIZE
        stop_index = from_index + PAGE_SIZE

        candidates_list = candidates_list[from_index:stop_index]

    if serialize:
        data = {"candidates": candidates_list, "total": len(candidates_list)}
        json_data = json.dumps(data)
        response = make_response(jsonify(data), 200)
        response.headers["ETag"] = str(hashlib.sha256(
            json_data.encode('utf-8')).hexdigest())
        response.headers["Cache-Control"] = "private, max-age=300"
        return response
    else:
        return candidates_list


@check_token
def candidate_by_id(candidate_id):
    """ Returns candidate based on an ID """

    candidate = DATA_PROVIDER.get_candidate(candidate_id, serialize=True)
    if candidate:
        return jsonify({"candidate": candidate})
    else:
        return make_response('', 404)


def add_candidate():
    """ Adds candidate to database """

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    phone = request.form["phone"]
    birthday = request.form["birthday"] if request.form["birthday"] is not None else ""

    new_candidate_id = DATA_PROVIDER.add_candidate(
        first_name=first_name,
        last_name=last_name,
        email=email,
        birthday=birthday,
        phone=phone)

    return jsonify({
        "id": new_candidate_id,
        "url": url_for("candidate_by_id", candidate_id=new_candidate_id)
    })


def update_candidate(candidate_id):
    """ Updates candidate """

    new_candidate = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "birthday": request.form["birthday"],
        "phone": request.form["phone"]
    }

    updated_candidate = DATA_PROVIDER.update_candidate(
        candidate_id, new_candidate)
    if not updated_candidate:
        return make_response('', 204)
    else:
        return jsonify({"candidate": updated_candidate})


def delete_candidate(candidate_id):
    """ Deletes candidate given an ID """
    try:
        if DATA_PROVIDER.delete_candidate(candidate_id):
            return make_response('', 204)
        else:
            return make_response('', 404)
    except ValueError as err:
        tmp_response = make_response("", 500)
        tmp_response.headers["X-APP-ERROR-CODE"] = get_error_code(str(err))
        tmp_response.headers["X-APP-ERROR-MESSAGE"] = err
        return tmp_response


def get_error_code(error):
    """ Gets error code """

    if "parameter" in error.lower():
        return 9100

    return 9000


def is_user_valid(username, password):
    """ Determines if user is provided is valid """
    return DATA_PROVIDER.is_user_valid(username, password)


def build_message(key, message):
    """ Returns message """
    return {key: message}

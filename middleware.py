""" Defines functions to fetch and return data """

from settings import Config
from data_provider_service import DataProviderService

from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for

db_engine = Config.DB_ENGINE

DATA_PROVIDER = DataProviderService(db_engine)


def initialize_database():
    """ Initializes database """
    DATA_PROVIDER.init_database()


def fill_database():
    """ Seeds database """
    DATA_PROVIDER.fill_database()


def candidates(serialize=True):
    """ Returns candidates """

    candidates_list = DATA_PROVIDER.get_candidate(serialize=serialize)
    if serialize:
        return jsonify({"candidates": candidates_list, "total": len(candidates_list)})
    else:
        return candidates_list


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
    birthday = request.form["birthday"]

    new_candidate_id = DATA_PROVIDER.add_candidate(
        first_name=first_name,
        last_name=last_name,
        email=email,
        birthday=birthday,
        phone=phone)

    return jsonify({
        "id": new_candidate_id,
        "url": url_for("candidate_by_id", id=new_candidate_id)
    })


def update_candidate(candidate_id):
    """ Updates candidate """

    new_candidate = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
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

    if DATA_PROVIDER.delete_candidate(candidate_id):
        return make_response('', 204)
    else:
        return make_response('', 404)


def build_message(key, message):
    """ Returns message """
    return {key: message}

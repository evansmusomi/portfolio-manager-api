""" Defines functions to fetch and return data """

from data_provider_service import DataProviderService
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for

DATA_PROVIDER = DataProviderService(15)


def candidates(serialize=True):
    """ Returns candidates """

    candidates_list = DATA_PROVIDER.get_candidates()
    if serialize:
        return jsonify({"candidates": candidates_list, "total": len(candidates_list)})
    else:
        return candidates_list


def candidate_by_id(candidate_id):
    """ Returns candidate based on an ID """

    candidate = DATA_PROVIDER.get_candidate(candidate_id)
    if candidate:
        return jsonify({"candidate": candidate})
    else:
        abort(404)


def delete_candidate(candidate_id):
    """ Deletes candidate given an ID """

    if DATA_PROVIDER.delete_candidate(candidate_id):
        return make_response('', 200)
    else:
        return abort(404)


def update_candidate_name(candidate_id, new_name):
    """ Updates candidates name

        Args:
            new_name: updated name
    """

    number_of_updated_items = DATA_PROVIDER.update_name(candidate_id, new_name)
    if number_of_updated_items == 0:
        abort(404)
    else:
        return jsonify({"total_updated": number_of_updated_items})


def random_candidates(number_of_items):
    """ Gets random number of candidates

        Args:
            number_of_items: number of random items to get (default = 1)
    """

    candidates_list = DATA_PROVIDER.get_random_candidates(number_of_items)
    return jsonify({"candidates": candidates_list, "total": len(candidates_list)})


def add_candidate():
    """ Adds candidate to database """

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]

    new_candidate_id = DATA_PROVIDER.add_candidate(first_name, last_name)

    return jsonify({
        "id": new_candidate_id,
        "url": url_for("candidate_by_id", id=new_candidate_id)
    })


def random_projects(number_of_items):
    """ Gets random number of projects """
    projects = DATA_PROVIDER.get_random_projects(number_of_items)
    return jsonify({"projects": projects, "total": len(projects)})


def add_project():
    """ Adds new project to database """

    project_name = request.form["name"]
    project_description = request.form["description"]

    new_project_id = DATA_PROVIDER.add_project(
        project_name, project_description)

    return jsonify({"id": new_project_id})

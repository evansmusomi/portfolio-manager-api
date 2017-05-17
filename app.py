""" Flask API definition """

from data_provider_service import DataProviderService
from flask import Flask
from flask import jsonify
from flask import url_for
from flask import abort
from flask import make_response
from flask import request


DATA_PROVIDER = DataProviderService(15)

# create Flask app
app = Flask(__name__)


# define routes

@app.route("/api", methods=['GET'])
def list_routes():
    """ Lists all API routes """
    result = []

    for route in app.url_map.iter_rules():
        result.append({
            "methods": list(route.methods),
            "route": str(route)
        })

    return jsonify({"routes": result, "total": len(result)})


@app.route("/api/candidates", methods=['GET'])
def candidates():
    """ Returns candidates """

    candidates_list = DATA_PROVIDER.get_candidates()
    return jsonify({"candidates": candidates_list, "total": len(candidates_list)})


@app.route("/api/candidates/<string:candidate_id>", methods=["GET"])
def candidate_by_id(candidate_id):
    """ Returns candidate based on an ID """

    candidate = DATA_PROVIDER.get_candidate(candidate_id)
    if candidate:
        return jsonify({"candidate": candidate})
    else:
        abort(404)


@app.route("/api/candidates/<string:candidate_id>/name/<string:new_name>", methods=["PUT"])
def update_name(candidate_id, new_name):
    """ Updates candidates name

        Args:
            new_name: updated name
    """

    number_of_updated_items = DATA_PROVIDER.update_name(candidate_id, new_name)
    if number_of_updated_items == 0:
        abort(404)
    else:
        return jsonify({"total_updated": number_of_updated_items})


@app.route("/api/random/candidates", defaults={"number_of_items": 1}, methods=["GET"])
@app.route("/api/random/candidates/<int:number_of_items>", methods=["GET"])
def random(number_of_items):
    """ Gets random number of candidates

        Args:
            number_of_items: number of random items to get (default = 1)
    """

    random_candidates = DATA_PROVIDER.get_random_candidates(number_of_items)
    return jsonify({"candidates": random_candidates, "total": len(random_candidates)})


@app.route("/api/candidates/delete/<string:candidate_id>", methods=["DELETE"])
def delete(candidate_id):
    """ Deletes candidate given an ID """

    if DATA_PROVIDER.delete_candidate(candidate_id):
        return make_response('', 200)
    else:
        return abort(404)


@app.route("/api/candidates", methods=["POST"])
def add_candidate():
    """ Adds candidate to database """

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]

    new_candidate_id = DATA_PROVIDER.add_candidate(first_name, last_name)

    return jsonify({
        "id": new_candidate_id,
        "url": url_for("candidate_by_id", id=new_candidate_id)
    })


if __name__ == "__main__":
    app.run(debug=True)

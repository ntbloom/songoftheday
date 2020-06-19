from flask import Flask, request, make_response, jsonify
from src import TEST_FLASK_PORT

app = Flask(__name__)


@app.route("/hello/", methods=["GET"])
def hello_world():
    """
    Can I connect to the database
    """
    return "Hello, world"


@app.route("/get-entries/", methods=["GET"])
def get_entries():
    """
    Query the API using database columns as params. Return data as JSON
    """
    pass


@app.route("/get-all-entries/", methods=["GET"])
def get_all_entries():
    """
    Get a JSON blob of all entries in the database
    """
    pass


@app.errorhandler(500)
def service_error():
    """returns 500 page"""
    return make_response(jsonify({"error": "Internal Service Error"}), 500)


@app.errorhandler(404)
def not_found():
    """returns 404 page"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.config["TESTING"] = True
    app.run(port=TEST_FLASK_PORT, debug=True, use_reloader=False)

from flask import Flask, request, make_response, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def create_entry():
    """
    Create an entry in the database. Returns entry_id as an int
    """
    pass


def get_entries():
    """
    Query the API using database columns as params. Return data as JSON
    """
    pass


def update_entry():
    """
    Update an entry in the database using the entry_id as the identifier
    """
    pass


def delete_entry():
    """
    Delete an entry based on its entry_id
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
    app.run(debug=True, use_reloader=False)

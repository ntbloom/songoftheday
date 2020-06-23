from flask import Flask, request, make_response, jsonify
from src import TEST_FLASK_PORT
from src.datastore.entry_wrapper import EntryWrapper
from typing import NamedTuple
from tests.conftest import TEST_DATABASE, HOST

app = Flask(__name__)


class PostgresParams(NamedTuple):
    database: str
    host: str


# configure the database for prod vs testing
production_database_ipaddress = ""  # TODO: update in production
postgres = (
    PostgresParams("sotd_production", production_database_ipaddress)
    if app.config["ENV"] == "production"
    else PostgresParams(TEST_DATABASE, HOST)
)


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
    entry_wrapper = EntryWrapper(postgres.database, postgres.host)
    entries = entry_wrapper.get_all_entries(**request.args)
    results = []
    for entry in entries:
        results.append(
            {
                "day": entry.day,
                "username": entry.username,
                "artist": entry.artist,
                "song_name": entry.song_name,
                "year": entry.year,
                "hyperlink": entry.hyperlink,
                "entered_at": entry.entered_at,
                "entry_id": entry.entry_id,
                "duration": entry.duration,
                "updated_at": entry.updated_at,
                "updated_by": entry.updated_by,
            }
        )
    return jsonify(results)


@app.errorhandler(500)
def service_error():
    """returns 500 page"""
    return make_response(jsonify({"error": "Internal Service Error"}), 500)


@app.errorhandler(404)
def not_found():
    """returns 404 page"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(port=TEST_FLASK_PORT, debug=True, use_reloader=False)

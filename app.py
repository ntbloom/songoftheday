from flask import Flask, request, make_response, jsonify
from src import TEST_FLASK_PORT, TEST_JWT_KEY, JWT_DAYS_VALID
from src.datastore.entry_wrapper import EntryWrapper
from typing import NamedTuple
from tests.conftest import TEST_DATABASE, HOST
from psycopg2.errors import UndefinedColumn
from src.postgres.password_manager import PasswordManager, PasswordError
from src.datastore.jwt_manager import Token, JWTManager

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

# configure secrets
if app.config["ENV"] == "production":
    pass  # TODO: read from .secrets file
else:
    jwt_key = TEST_JWT_KEY


@app.route("/v1.0/hello/", methods=["GET"])
def hello_world():
    """
    Can I connect to the database
    """
    return "Hello, world"


@app.route("/v1.0/get-entries/", methods=["GET"])
def get_entries():
    """
    Query the API using database columns as params. Return data as JSON
    """
    with EntryWrapper(postgres.database, postgres.host) as entry_wrapper:
        args: dict = request.args.to_dict()
        fuzzy = args.pop("fuzzy", False)
        try:
            entries = entry_wrapper.get_all_entries(fuzzy, **args)
            if not entries:
                return make_response(jsonify({"error": "no results"}), 204)
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
            return make_response(jsonify(results), 200)
        except UndefinedColumn:
            return make_response(jsonify({"error": "illegal query params"}), 400)


@app.route("/v1.0/authenticate/", methods=["POST"])
def authenticate():
    """
    Validate the password in postgres, return a valid JWT token
    """
    args = request.args.to_dict()
    username = args["username"]
    password = args["password"]
    with PasswordManager(postgres.database, postgres.host) as password_manager:
        try:
            level = password_manager.authenticate_with_password(username, password)
        except PasswordError:
            return make_response(jsonify({"error": "Authentication Error"}), 403)
        token = Token(username, level)
        jwt_manager = JWTManager(jwt_key)
        encrypted_token = jwt_manager.encrypt(token)
        return encrypted_token


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

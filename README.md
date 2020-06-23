# Song of the Day

A web app using a simple Postgresql database to track sharing a new song every
day between friends.

More details to come as project gets developed. Current work is on the back end
which should be completed relatively soon.

---

### Dependencies

- podman with `docker.io/library/postgres` image downloaded
  - docker should work if you put `alias podman="docker"` in your .bashrc
- python 3.8
- nodejs 12.16

<br>

---

<br>

### Back End

A bare-bones Flask/Postgres REST API

<br>

#### Run the test suite:

Enable a postgres container:

```console
user@host:~/$ podman run --rm \
    --name sotd_test \
    -e POSTGRES_PASSWORD=docker \
    -d \
    -p 5432:5432 \
    docker.io/library.postgres
```

Run all of the tests on the back end. 

```console
user@host:~/songoftheday$ npm run pytest
```

The text fixtures will automatically create a new database instance with sample data 
loaded, so when a single test run is complete the database will be ready for use.

<br>

#### Enable a dev server for the API

To run the API locally, either run the test suite first to populate the database, or 
instantiate a testing database by using the DataPopulator class.

```console
user@host~/songoftheday$ venv/bin/python src/datastore/data_populator.py # optional 
user@host:~/songoftheday$ npm run flask-dev
```

Access the dev server at [http://localhost:5000/get-entries/](http://localhost:5000/get-entries/)

<br>

---

<br>

### Front End

<br>

coming soon...

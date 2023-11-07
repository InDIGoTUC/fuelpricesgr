# Fuel Prices

The purpose of this project is to create a database of fuel prices in Greece. Daily and weekly data about fuel prices
are regularly uploaded at the [Παρατηρητήριο Τιμών Υγρών Καυσίμων](http://www.fuelprices.gr) website by the Greek
Government, but the data are published as PDF files. In order to process the data more easily, this project fetches
those PDF files, extracts the data from them, inserts them in a database, and exposes them in an API.

## Running the API

The backend API is a [Python](https://www.python.org) based project, built with
[FastAPI](https://fastapi.tiangolo.com), that uses [Poetry](https://python-poetry.org) for dependency management. In
order to install the dependencies, you need to run:

```
poetry install
```

The data are stored in an [SQLite](https://www.sqlite.org) database. In order to fetch the data you need to run:

```
python -m fuelpricesgr.commands.import
```

This command accepts various parameters to limit the data to be fetched. You can see them by running

```
python -m fuelpricesgr.commands.import --help
```

Now you can launch the API by running the command:

```
uvicorn fuelpricesgr.main:app
```

The API is now available at http://localhost:8000. The documentation for the API is available at
http://localhost:8000/docs.

## Running the frontend

A simple front end has been developed. The project dependencies are manages by [npm](https://www.npmjs.com), so you
need to change to the `frontend` directory and run:

```
npm install
```

Then you can launch the frontend with:

```
npm start
```

This command will launch the frontend at http://localhost:8080.

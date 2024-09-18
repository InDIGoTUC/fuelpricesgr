# Fuel Prices

The purpose of this project is to create a database of fuel prices in Greece. Daily and weekly data about fuel prices are regularly uploaded at the [Παρατηρητήριο Τιμών Υγρών Καυσίμων](http://www.fuelprices.gr) website by the Greek Government, but the data are published as PDF files. In order to process the data more easily, this project fetches those PDF files, extracts the data from them, inserts them into a database, and exposes them through an API.

Data are available since:

* 2012-04-27 for weekly country data
* 2012-05-04 for weekly prefecture data
* 2017-08-28 for daily country data
* 2017-03-14 for daily prefecture data

## Running the API

The backend API is a [Python](https://www.python.org) project, built with [FastAPI](https://fastapi.tiangolo.com), and uses [Poetry](https://python-poetry.org) for dependency management. To install the dependencies, run:

```sh
poetry install
```

Data is stored in an [SQLite](https://www.sqlite.org) database. To fetch the data, use:

```sh
python -m fuelpricesgr.commands.import
```

This command supports various parameters to limit the data to be fetched:

```sh
python -m fuelpricesgr.commands.import --help
```

To launch the API:

```sh
uvicorn fuelpricesgr.main:app
```

The API will be available at http://localhost:3002, with documentation at http://localhost:3002/docs.

## Running with Docker

To make the setup easier, a Docker image is provided. This allows running the API as a self-contained service with minimal setup.

### Building the Docker Image

First, build the Docker image:

```sh
docker build -t fuelpricesgr .
```

### Running the Docker Image

Run the Docker container:

```sh
docker run -p 3002:8000 fuelpricesgr
```

This will expose the API on `localhost:3002`. You can access the API documentation at `http://localhost:3002/docs`.

### Running the Import Command in Docker

To run the import command inside the Docker container, use:

```sh
docker exec -it <container_name> python -m fuelpricesgr.commands.import --start-date {YYYY-MM-DD} --end-date {YYYY-MM-DD}
```

### Automating the Import with Docker

To set up automated daily updates for fuel prices, modify your Docker container or orchestrate it with a task scheduler (like a cron job in Docker) to run the import command with the `--update` flag:

```sh
python -m fuelpricesgr.commands.import --update
```

## API Endpoints

### Basic API Functions

| Method | Endpoint | Parameters | Description |
| ------ | -------- | ---------- | ----------- |
| GET    | `/status` | None       | Returns the status of the application |
| GET    | `/fuelTypes` | None   | Returns all fuel types |
| GET    | `/prefectures` | None | Returns all prefectures |
| GET    | `/dateRange/{data_type}` | None | Get the available data date range for a specific data type |

### Getting Fuel Data

| Method | Endpoint                                | Query Parameters     | Description                                 |
| ------ | --------------------------------------- | -------------------- | ------------------------------------------- |
| GET    | `/data/daily/country`                   | start_date, end_date | Returns the daily country data (for Greece) |
| GET    | `/data/daily/prefectures/{prefecture}`  | start_date, end_date | Returns the daily prefecture data           |
| GET    | `/data/weekly/country`                  | start_date, end_date | Returns the weekly country data (for Greece)|
| GET    | `/data/weekly/prefectures/{prefecture}` | start_date, end_date | Returns the weekly prefecture data          |

### API Usage Example

To fetch daily fuel data for a specific prefecture between two dates:

```sh
GET /data/daily/prefectures/ATTICA?start_date=2023-01-01&end_date=2023-01-31
```

## Development

To run the application tests:

```sh
pytest
```

To get a test coverage report:

```sh
coverage run -m pytest .
```

This will generate an HTML coverage report in `htmlcov/index.html`.

To get a pylint report:

```sh
pylint fuelpricesgr
```

## Additional Notes

- The API exposes endpoints for fuel prices on a daily and weekly basis for both the country and individual prefectures.
- To limit the data to daily prices, use the following command to fetch only `DAILY_COUNTRY` and `DAILY_PREFECTURE` data:

```sh
python -m fuelpricesgr.commands.import --types DAILY_COUNTRY,DAILY_PREFECTURE --start-date {YYYY-MM-DD} --end-date {YYYY-MM-DD}
```

- To configure email notifications for data updates, create a `.env` file in the root of the project folder with the following content:

```sh
SECRET_KEY={SECRET_KEY}
MAIL_SENDER={MAIL_SENDER}
MAIL_RECIPIENT={MAIL_RECIPIENT}
```

Then run the import command with the `--send-mail` flag to trigger an email notification:

```sh
python -m fuelpricesgr.commands.import --send-mail
```


"""The FastAPI main module
"""
import datetime
import itertools
import typing

import fastapi
import fastapi.middleware.cors

from fuelpricesgr import database

app = fastapi.FastAPI()
app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=["http://127.0.0.1:8080", "http://localhost:8080"],
)


# The maximum number of days to return from the API
MAX_DAYS = 365


@app.get("/")
async def index() -> dict:
    """Returns the status of the application.
    """
    return {"status": "OK"}


@app.get("/data/dailyCountry")
async def daily_country_data(
        start_date: datetime.date | None = None, end_date: datetime.date | None = None) -> typing.List[dict]:
    """Returns daily country averages.
    """
    # Make sure that we don't get more days than MAX_DAYS
    if start_date is None and end_date is None:
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=MAX_DAYS)
    elif start_date is None:
        start_date = end_date - datetime.timedelta(days=MAX_DAYS)
    elif end_date is None:
        end_date = start_date + datetime.timedelta(days=MAX_DAYS)
    elif start_date > end_date:
        raise fastapi.HTTPException(status_code=400, detail="Start date must be before end date")
    else:
        days = (end_date - start_date).days
        start_date = end_date - datetime.timedelta(days=min(days, MAX_DAYS))

    with database.Database(read_only=True) as db:
        return [
            {
                'date': date,
                'results': [
                    {
                        'fuel_type': row['fuel_type'],
                        'number_of_stations': row['number_of_stations'],
                        'price': row['price'],
                    } for row in date_group
                ]
            } for date, date_group in itertools.groupby(
                db.daily_country_data(start_date=start_date, end_date=end_date), lambda x: x['date']
            )
        ]

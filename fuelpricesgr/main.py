"""The FastAPI main module
"""
import fastapi.middleware

from fuelpricesgr import settings, views

app = fastapi.FastAPI(
    title="Fuel Prices in Greece",
    description="""
    An API that returns data for fuel prices in Greece. Daily and weekly data about fuel prices are regularly
    uploaded at the [Παρατηρητήριο Τιμών Υγρών Καυσίμων](http://www.fuelprices.gr/) website by the Greek Government, but
    the data are published as PDF files. With this API you can get the data in a structured manner.""",
    contact={
        "name": "Kostas Kokkoros",
        "url": "https://www.mavroprovato.net",
        "email": "mavroprovato@gmail.com",
    },
    license_info={
        "name": "The MIT License (MIT)",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url=None,
    redoc_url='/docs',
)
app.include_router(views.api.router)

# Add SQL admin if the backend is SQL Alchemy
if settings.STORAGE_BACKEND == 'fuelpricesgr.storage.sql_alchemy.SqlAlchemyStorage':
    import sqladmin
    import fuelpricesgr.storage.sql_alchemy
    import fuelpricesgr.views.admin

    admin = sqladmin.Admin(
        app, fuelpricesgr.storage.sql_alchemy.get_engine(),
        authentication_backend=fuelpricesgr.views.admin.AuthenticationBackend(secret_key=settings.SECRET_KEY)
    )
    admin.add_view(fuelpricesgr.views.admin.DailyCountryAdmin)
    admin.add_view(fuelpricesgr.views.admin.DailyPrefectureAdmin)
    admin.add_view(fuelpricesgr.views.admin.WeeklyCountryAdmin)
    admin.add_view(fuelpricesgr.views.admin.WeeklyPrefectureAdmin)
    admin.add_view(fuelpricesgr.views.admin.UserAdmin)

### A django application using the Django Rest Framework that registers and returns device data.

#### The API contains one endpoint

    http://127.0.0.1:8000/device/

    Docs: http://127.0.0.1:8000/device/swagger/

The POST method acceps a reading from a device.

    Example payload:
        [
            {
                "timestamp": "RFC3339 Datetime string",
                "reading": float,
                "device_id": "UUIDv4 string",
                "customer_id": "UUIDv4 string"
            },
        ...
        ]


The GET method retuns the aggregated data from a device over a period of 5 mins(default)

This default aggregate_size can be modified with a query param agg_size



### Accepted query params: 

    device_id (example 23706ac3-88c4-45a4-9ca0-427d7f162cdb)

    customer_id (example 2140c6cf-f513-489c-b49f-a8686582c664)

    start_time (example start_time=2021-11-20T14:25:00Z; defaults to no lower limit if not present)

    end_time (example start_time=2021-11-20T14:25:00Z; defaults to no upper limit if not present)

    agg_size (example 10)

http://127.0.0.1:8000/device/?device_id=23706ac3-88c4-45a4-9ca0-427d7f162cdb&agg_size=10

http://127.0.0.1:8000/device/?customer_id=23706ac3-88c4-45a4-9ca0-427d7f162cdb


### How to run this app


1. Install python

2. Install Django

3. run `pip install -r requirements.txt`

4. This will install all the required dependencies

    Database connection

    The app uses a postgres DB, default schema to work.

    Please update the DB configs in the settings.py -> DATABASE part

5. Run `python manage.py runserver`

6. The web ui can be seen at `http://127.0.0.1:8000/device/`

### Assumptions/Enhancements
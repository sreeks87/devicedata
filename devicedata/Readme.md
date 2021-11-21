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


### Screenshots

Available in the screenshot folder

### How to run this app


1. Install python

2. Install Django

3. run `pip install -r requirements.txt`

4. This will install all the required dependencies

5. Database connection

        The app uses a postgres DB, default schema to work.

        Please update the DB configs in the settings.py -> DATABASE part

        The DB values could be setup as env variables

6. Run `python manage.py runserver`

7. The web ui can be seen at `http://127.0.0.1:8000/device/`

### Example

    POST http://127.0.0.1:8000/device/
    [
        {
            "timestamp": "2021-11-20T14:25:00Z",
            "reading": 158.323,
            "device_id": "1dae7442-a8ac-47d8-83f9-70672cdb0694",
            "customer_id": "1dae7442-a8ac-47d8-83f9-70672cdb0694"
        }
    ]



    GET http://127.0.0.1:8000/device/

    {
    "data": [
        {
            "device_id": "1dae7442-a8ac-47d8-83f9-70672cdb0694",
            "customer_id": "1dae7442-a8ac-47d8-83f9-70672cdb0694",
            "readings": [
                {
                    "timestamp": "2021-11-20T14:25:00Z",
                    "reading": 158.323
                }
            ]
        },
        {
            "device_id": "a7986ad6-896b-47d8-9dc7-f1d38fdecb4b",
            "customer_id": "27d93758-4e25-4919-9a2b-b1ec0b281b65",
            "readings": [
                {
                    "timestamp": "2021-11-21T15:20:00Z",
                    "reading": 4407.4400000000005
                },
                {
                    "timestamp": "2021-11-21T16:20:00Z",
                    "reading": 135.56
                },
                {
                    "timestamp": "2021-11-21T17:20:00Z",
                    "reading": 13.56
                }
            ]
        }
    ]
}

### Assumptions/Enhancements

1. Customer ID and Device ID in the table can be non unique, there will be multiple reading from same devices for same same/different customers.

2. None of the fields can be null.

3. For this requirement - "data should be retrievable by Device and Customer (for all devices related to that customer)"

    An assumption has been made that the device_id or customer_id will be passed as a query param tothe same endpoint. There is no separate endpoint defined for fetching the data for device_id or customer_id.

    Expected url qury parameters:

    ?customer_id=\<uuid customer_id> 
    
    or

    ?device_id=\<uuid device_id>


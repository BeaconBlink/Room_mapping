# Mapping server and the machine learning module

## Machine learning module
This module is responsible for estimating the location of the Beacon devices.
It uses data from the database gathered through room calibration.
<br>
Model trained after every new room calibartion and every room deletion to ensure data consitency.
### Used model
We used KNN (k-nearest neighbours) algorithm to estimate the location of the Beacon devices.
The KNN algorithm is a simple and effective machine learning algorithm used for classification and regression tasks.
In our implementation number of neighbours is equal 2.

### Tech stack
- Python (version: 3.12.4)
- SciKit-Learn

## Mapping server

This server provides communication between the main server and the machine learning module.

### Tech stack
- Python (version: 3.12.4)
- Uvicorn
- FastAPI

## Starting the server:

### It is not recommended to run the server alone. Be sure to run the whole [Deployment](https://github.com/BeaconBlink/Deployment).

### Installing the virtual environment
```bash
  pip install virtualenv
```
### Create virtual environment (first usage)
``` bash
    virtualenv .venv
```
### Activate virtual environemnt
```bash
  source ./.venv/Scripts/activate
```
### Get all the requriements
```bash
  pip install -r requirements.txt
```
### Development start Python server
```bash
  uvicorn Server:app --host 0.0.0.0 --port 8083 --reload
```

## Available Endpoints

### `POST "/location"`

Returns the identifier of the predicted location based on the received data. If the model has not been previously trained, an error with code `503` will be returned as a response.

#### Arguments:
- `scan_results`: **NetworkInfo[]** - Information about networks scanned by the Beacon.

#### Response:
- Room identifier **string**.

### `POST "/retrain"`

Allows clearing the currently saved model, and then initiates retraining using the latest information stored in the database.
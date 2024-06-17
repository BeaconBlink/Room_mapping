# Python environemnt

Python version: 3.12.4

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
# import Room_mapping
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()
# RM = Room_mapping.RoomMapper()

class NetworkInfo(BaseModel):
    ssid: str
    rssi: int
    bssid: str

class NetworskInfo(BaseModel):
    mac_address: str
    scan_results: Optional[List[NetworkInfo]] = None

@app.post("/location/")
def create_item(networksInfo: NetworskInfo):
    return {"name": "d17"}

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8083)
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import Room_mapping

app = FastAPI()
RM = Room_mapping.RoomMapper()


class NetworkInfo(BaseModel):
    ssid: str
    rssi: int
    bssid: str


class NetworksInfo(BaseModel):
    scan_results: Optional[List[NetworkInfo]] = None


class ChangeModeBody(BaseModel):
    mode: bool


@app.post("/location/mode")
def change_mode(body: ChangeModeBody):
    print("MODE: ", body.mode, flush=True)
    if not RM.trained() and body.mode:
        RM.train()
    return {"trained": True}


@app.post("/location")
def get_room_prediction(networks_info: NetworksInfo):
    if not RM.trained():
        raise HTTPException(status_code=404, detail="Model is not trained yet")

    room = RM.get_device_location(networks_info)
    return {"id": room}

@app.post("retrain")
def retrain_model():
    RM.retrain()
    return {"retrained": True}

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8083)

import Room_mapping
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()
RM = Room_mapping.RoomMapper()

class NetworkInfo(BaseModel):
    ssid: str
    rssi: int
    bssid: str

class NetworksInfo(BaseModel):
    scan_results: Optional[List[NetworkInfo]] = None

@app.post("/location/")
def getRoomPrediction(networksInfo: NetworksInfo):
    if not RM.trained():
        RM.train()
        raise HTTPException(status_code=404, detail="Model is not trained yet")
    
    room = RM.getDeviceLocation(networksInfo)
    return {"name": room}

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8083)

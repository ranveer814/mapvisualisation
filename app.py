import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json

app = FastAPI()

# Store connected WebSocket clients
active_connections = []

# Define the data model for incoming data
class LocationData(BaseModel):
    name: str
    uniqueID: str
    floor: int
    latitude: float
    longitude: float

@app.websocket("/track")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            location_data = json.loads(data)

            # Broadcast the location data to all connected clients
            for connection in active_connections:
                await connection.send_text(data)
    except WebSocketDisconnect:
        active_connections.remove(websocket)

@app.get("/")
async def get():
    return HTMLResponse(open("index.html").read())

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

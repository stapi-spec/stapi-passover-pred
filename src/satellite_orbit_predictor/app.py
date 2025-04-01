from fastapi import FastAPI, HTTPException, Query
from skyfield.api import load
from datetime import datetime
import uvicorn
from contextlib import asynccontextmanager

app = FastAPI()

ACTIVE_SATS_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active"

@asynccontextmanager
async def lifespan(app: FastAPI):
    global satellites, ts
    satellites = {sat.model.satnum: sat for sat in load.tle_file(ACTIVE_SATS_URL)}
    ts = load.timescale()
    yield
    satellites = None
    ts = None

app = FastAPI(lifespan=lifespan)

@app.get("/predict")
def predict_satellite(
    satellite: int = Query(..., description="NORAD ID of the satellite"),
    temporal: datetime = Query(..., description="Date-time in ISO format, e.g., '2025-04-01T12:00:00Z'")
):
    sat = satellites.get(int(satellite))

    # Predict position
    t = ts.from_datetime(temporal)
    geocentric = sat.at(t)
    subpoint = geocentric.subpoint()

    return {
        "satellite": sat.name,
        "datetime": temporal.isoformat() + "Z",
        "latitude": subpoint.latitude.degrees,
        "longitude": subpoint.longitude.degrees,
        "altitude": subpoint.elevation.km,
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

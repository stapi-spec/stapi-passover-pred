from fastapi import FastAPI, Body, Path, Request
from skyfield.api import load, wgs84, utc
import uvicorn
from contextlib import asynccontextmanager
from stapi_pydantic import OpportunityPayload

ACTIVE_SATS_URL = "http://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"

constellations = {
    "orbital-sidekick": {"GHOST-1":56195, "GHOST-2":56197, "GHOST-3":56958, "GHOST-4":59133, "GHOST-5":59130},
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield {"ts": load.timescale(), "satellites": {sat.name: sat for sat in load.tle_file(ACTIVE_SATS_URL)}}

app = FastAPI(lifespan=lifespan)

@app.post("/products/{constellation}/opportunities")
def opportunities(
    request: Request,
    constellation: str = Path(..., description="Constellation name"),
    opportunity: OpportunityPayload = Body(..., description="Opportunity payload"),
):
    start_time = request.state.ts.from_datetime(opportunity.datetime[0].replace(tzinfo=utc))
    end_time = request.state.ts.from_datetime(opportunity.datetime[1].replace(tzinfo=utc))
    location = wgs84.latlon(opportunity.geometry.coordinates[1], opportunity.geometry.coordinates[0])
    passes = []

    for satellite_name in constellations[constellation]:
        satellite = request.state.satellites[satellite_name]
        t, events = satellite.find_events(location, start_time, end_time, altitude_degrees=50.0)

        for ti, event in zip(t, events):
            if event == 0:
                difference = satellite - location
                topocentric = difference.at(ti)

                _, az, _ = topocentric.altaz()

                sat_pos = satellite.at(ti)
                subpoint = wgs84.subpoint(sat_pos)

                pass_info = {
                    "satellite": satellite_name,
                    "datetime": ti.utc_datetime().strftime("%Y-%m-%dT%H:%M:%S"),
                    "altitude": subpoint.elevation.km,
                    "azimuth": az.degrees
                }
                passes.append(pass_info)

    return passes

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
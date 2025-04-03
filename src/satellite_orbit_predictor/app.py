import uvicorn
from fastapi import FastAPI, Body, Path, Request
from skyfield.api import load, wgs84, utc
from contextlib import asynccontextmanager
from stapi_pydantic import OpportunityPayload, OpportunityCollection, Opportunity, Link, OpportunityProperties
from geojson_pydantic.geometries import Point

ACTIVE_SATS_URL = "http://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"

constellations = {
    "orbital-sidekick": {"GHOST-1":56195, "GHOST-2":56197, "GHOST-3":56958, "GHOST-4":59133, "GHOST-5":59130},
    "sentinel-1": {'SENTINEL-1A': 39634, 'SENTINEL-1B': 41456, 'SENTINEL-1C': 62261},
    "sentinel-2": {'SENTINEL-2A': 40697, 'SENTINEL-2B': 42063, 'SENTINEL-2C': 60989},
    "sentinel-3": {'SENTINEL-3A': 41335, 'SENTINEL-3B': 43437},
    "blacksky": {'GLOBAL-2': 43812, 'GLOBAL-4': 44499, 'GLOBAL-9': 47971, 'GLOBAL-14': 49469, 'GLOBAL-12': 49772,
                 'GLOBAL-13': 49773, 'GLOBAL-17': 49949, 'GLOBAL-16': 49950, 'GLOBAL-18': 52196, 'GLOBAL-19': 55982,
                 'GLOBAL-5': 55983, 'GLOBAL-31': 63027},
    "landsat": {'LANDSAT 1 (ERTS 1)': 6126, 'LANDSAT 2': 7615, 'LANDSAT 3': 10702, 'LANDSAT 4': 13367,
                'LANDSAT 5': 14780, 'LANDSAT 7': 25682, 'LANDSAT 8': 39084, 'LANDSAT 9': 49260}
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
) -> OpportunityCollection:
    start_time = request.state.ts.from_datetime(opportunity.datetime[0].replace(tzinfo=utc))
    end_time = request.state.ts.from_datetime(opportunity.datetime[1].replace(tzinfo=utc))
    location = wgs84.latlon(opportunity.geometry.coordinates[1], opportunity.geometry.coordinates[0])
    passes = []

    for satellite_name in constellations[constellation]:
        satellite = request.state.satellites[satellite_name]
        t, events = satellite.find_events(location, start_time, end_time, altitude_degrees=50.0)

        for i, (ti, event) in enumerate(zip(t, events)):
            if event == 1:
                difference = satellite - location
                topocentric = difference.at(ti)

                _, az, _ = topocentric.altaz()

                sat_pos = satellite.at(ti)
                subpoint = wgs84.subpoint(sat_pos)
                passes.append(
                    Opportunity(
                        geometry=Point(type="Point", coordinates=[opportunity.geometry.coordinates[0], opportunity.geometry.coordinates[1]]),
                        properties=OpportunityProperties(
                            satellite=satellite_name,
                            datetime=(t[i-1].utc_datetime(), t[i+1].utc_datetime()),
                            altitude=subpoint.elevation.km,
                            azimuth=az.degrees,
                            product_id=constellation,
                        ),
                        id=satellite_name
                    )
                )

    return OpportunityCollection(features=passes, links=[Link(href=ACTIVE_SATS_URL, rel="via")])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

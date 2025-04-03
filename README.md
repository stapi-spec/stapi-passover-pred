# Satellite Orbit Predictor API

FastAPI service that predicts satellite positions using CelesTrak data.

## Quick Start

```bash
# Install dependencies
uv sync

# Run server
uv run uvicorn src.satellite_orbit_predictor.app:app --host 0.0.0.0 --port 8000 --reload
```

Server runs at `http://localhost:8000`

## API Usage

```bash
# Predict satellite position
curl -X POST "http://localhost:8000/products/orbital-sidekick/opportunities" \
  -H "Content-Type: application/json" \
  -d '{
    "datetime": "2025-04-11T00:00:00Z/2025-04-12T00:00:00Z",
    "geometry": {
      "type": "Point",
      "coordinates": [13.4050, 52.5200]
    },
    "filter": null,
    "limit": 10
  }'
```

Response:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [13.405, 52.52]
      },
      "properties": {
        "datetime": "2025-04-11T22:33:12.760224+00:00/2025-04-11T22:34:40.473005+00:00",
        "product_id": "orbital-sidekick",
        "satellite": "GHOST-1",
        "altitude": 428.3845855309221,
        "azimuth": 103.11218045332878
      },
      "id": "GHOST-1",
      "links": []
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [13.405, 52.52]
      },
      "properties": {
        "datetime": "2025-04-11T22:31:19.470434+00:00/2025-04-11T22:31:54.260710+00:00",
        "product_id": "orbital-sidekick",
        "satellite": "GHOST-2",
        "altitude": 404.863092712036,
        "azimuth": 100.79918372810874
      },
      "id": "GHOST-2",
      "links": []
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [13.405, 52.52]
      },
      "properties": {
        "datetime": "2025-04-11T00:43:20.412142+00:00/2025-04-11T00:44:47.884168+00:00",
        "product_id": "orbital-sidekick",
        "satellite": "GHOST-4",
        "altitude": 484.4707649864979,
        "azimuth": 257.96599673620267
      },
      "id": "GHOST-4",
      "links": []
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [13.405, 52.52]
      },
      "properties": {
        "datetime": "2025-04-11T13:36:23.023887+00:00/2025-04-11T13:37:45.005056+00:00",
        "product_id": "orbital-sidekick",
        "satellite": "GHOST-4",
        "altitude": 491.14467955791997,
        "azimuth": 101.88144667577255
      },
      "id": "GHOST-4",
      "links": []
    }
  ],
  "links": [
    {
      "href": "http://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle",
      "rel": "via"
    }
  ],
  "id": null
}
```

## Documentation

- Data source: CelesTrak stations feed
- All coordinates in degrees, altitude in km

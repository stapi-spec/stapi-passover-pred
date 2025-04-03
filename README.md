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
[
  {"satellite":"GHOST-1","datetime":"2025-04-11T22:33:12","altitude":429.07439378005614 "azimuth":28.574388573135575},
  {"satellite":"GHOST-2","datetime":"2025-04-11T22:31:19","altitude":405.1201764276592,"azimuth":77.10403184757281},
  {"satellite":"GHOST-4","datetime":"2025-04-11T00:43:20","altitude":483.50380330533676,"azimuth":199.82511673545932},
  {"satellite":"GHOST-4","datetime":"2025-04-11T13:36:23","altitude":491.647469776105,"azimuth":50.18517804815514}
]
```

## Documentation

- API docs: http://localhost:8000/docs
- Data source: CelesTrak stations feed
- All coordinates in degrees, altitude in km

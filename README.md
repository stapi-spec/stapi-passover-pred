# Satellite Orbit Predictor API

FastAPI service that predicts satellite positions using CelesTrak data.

## Quick Start

```bash
# Install dependencies
uv pip install -r requirements.txt

# Run server
uv run uvicorn src.satellite_orbit_predictor.app:app --host 0.0.0.0 --port 8000 --reload
```

Server runs at `http://localhost:8000`

## API Usage

```bash
# Predict satellite position
curl "http://localhost:8000/predict?satellite=ISS&datetime_str=2025-04-01T12:00:00Z"
```

Response:
```json
{
    "satellite": "ISS (ZARYA)",
    "datetime": "2025-04-01T12:00:00Z",
    "latitude": 51.6417,
    "longitude": -0.1337,
    "altitude": 408.05
}
```

## Documentation

- API docs: http://localhost:8000/docs
- Data source: CelesTrak stations feed
- All coordinates in degrees, altitude in km

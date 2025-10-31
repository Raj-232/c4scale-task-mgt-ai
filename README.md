# c4scale - Dockerized Setup

This repository includes a FastAPI backend and a Next.js UI, packaged with Docker and docker-compose. A PostgreSQL database is provided via Docker as well.

## Services
- Backend (FastAPI): http://localhost:8000/api/v1
- WebSocket: ws://localhost:8000/api/v1/chat
- UI (Next.js): http://localhost:3000
- Database (Postgres): localhost:5432 (inside compose network as `postgres`)

## Quick Start

1) Ensure Docker and Docker Compose are installed.

2) Build and start all services:

```bash
docker compose up --build -d
```

3) Open the UI:

```bash
http://localhost:3000
```

The UI communicates with the backend using environment variables baked into the container:
- `NEXT_PUBLIC_API_BASE` defaults to `http://backend:8000/api/v1`
- `NEXT_PUBLIC_WS_BASE` defaults to `ws://backend:8000/api/v1/chat`

These are configured in `docker-compose.yaml` for the `ui` service.

## Environment Variables

The backend reads configuration from environment variables (see `backend/app/utils/config_env.py`):
- `POSTGRES_HOST`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_PORT`, `POSTGRES_DB`
- Optional: `GOOGLE_API_KEY`

By default, `docker-compose.yaml` wires the backend to the `postgres` service with user/password/db set to `postgres`.

If you want to pass a Google API key at runtime:

```bash
GOOGLE_API_KEY=your_key_here docker compose up --build -d
```

## Stopping and Cleaning Up

```bash
docker compose down
```

Remove volumes if you want to reset the database:

```bash
docker compose down -v
```

## Directory Notes

The frontend directory is named `forntend` in this repository. Docker Compose is already configured to build from that directory.

## Development Notes

- Backend container runs `uvicorn app.main:app` on port 8000.
- UI container runs `next start` on port 3000.
- Postgres is exposed on port 5432 for local tools if needed.



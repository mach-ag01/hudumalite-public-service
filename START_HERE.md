# Start Here — HudumaLite

This folder contains the complete React + Django + PostgreSQL project. Do not upload the ZIP itself into your source repository. Extract it first, then upload the **contents** so that `README.md`, `frontend/`, and `backend/` are visible at the repository root.

## Quick map
- `frontend/` — React website; deploy this directory to Vercel.
- `backend/` — Django REST API; deploy to Render or Railway.
- `render.yaml` — starter configuration for the API and a managed Postgres database on Render.
- `README.md` — full setup, endpoints, testing, and deployment instructions.

## Required deployment order
1. Upload all project contents to GitHub and commit.
2. Create PostgreSQL and deploy the Django API.
3. Set the API's CORS origin to your Vercel domain.
4. Import the repository into Vercel with Root Directory `frontend`.
5. Set `VITE_API_URL` to the deployed API URL ending in `/api` and redeploy.
6. Create a Django superuser to use the staff dashboard.

A successful Vercel build alone does not deploy the Django API or provision PostgreSQL; those are separate services in this architecture.

## Security and scaling additions

- API throttling: anonymous/user global limits plus stricter registration, login, and request-creation scopes.
- Shared counters: configure `REDIS_URL` for Redis-backed rate limiting when deployed across multiple API instances.
- Proxy limits/load balancing template: `infra/nginx/hudumalite.conf` demonstrates per-IP request and connection limits and `least_conn` balancing across two private API instances. Replace the example IPs and set up TLS before using it.
- Production security settings: HTTPS redirect, secure cookies, HSTS, content-type sniffing protection, frame protection, environment-based host/CORS allowlists.

These are baseline protections, not a security certification. Production use still needs proper secrets management, monitored logging, backups, durable image storage, vulnerability updates, and load/security testing.

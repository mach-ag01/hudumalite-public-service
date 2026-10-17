# HudumaLite — Public Service Request System

A full-stack Mini eCitizen-style service request platform built with **React + Vite**, **Django REST Framework**, and **PostgreSQL**. It supports citizen accounts, service requests, optional image uploads, request tracking, staff status updates, and analytics.

> **Deployment architecture:** deploy the React frontend to Vercel. Deploy the Django API to a Python application host such as Render or Railway, and use a managed PostgreSQL database such as Neon, Supabase, Render Postgres, or Railway Postgres. Vercel is excellent for the frontend, but a conventional long-running Django application and persistent uploaded media are better hosted separately. Configure `VITE_API_URL` to point at the deployed API.

## Features

- Citizen registration and JWT login
- Citizen dashboard with request reference IDs and status tracking
- Create a request with category, location, description, and optional image
- Categories: Roads, Water, Street Lighting, Waste Collection, Drainage, Other
- Request status workflow: Pending → In Progress → Resolved
- Staff/admin request management and status history
- Search and filter requests by status/category
- Analytics for total, open, in-progress, and resolved cases
- Responsive layout and accessible form labels
- Django admin, API pagination, validation, CORS configuration, environment-based secrets
- API tests for permissions and core request behaviour

## Project structure

```text
hudumalite-fullstack/
├── frontend/                 # React + Vite SPA
│   ├── src/
│   ├── .env.example
│   └── package.json
├── backend/                  # Django REST API
│   ├── config/
│   ├── requests_api/
│   ├── requirements.txt
│   └── .env.example
├── render.yaml               # Example Django API deployment blueprint
└── README.md
```

## Run locally

### Requirements

- Node.js 20+
- Python 3.11+
- PostgreSQL 14+ (or a PostgreSQL connection string from a managed provider)

### 1. Start the backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env`, then set `DATABASE_URL` to your PostgreSQL URL and change `DJANGO_SECRET_KEY`. For local development, you can use SQLite by setting `DATABASE_URL` blank; PostgreSQL is recommended for evaluation and deployment.

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API runs at `http://127.0.0.1:8000/api/`. Django admin is at `http://127.0.0.1:8000/admin/`.

### 2. Start the frontend

In another terminal:

```bash
cd frontend
npm install
```

Copy `frontend/.env.example` to `frontend/.env` (the default API URL works locally), then run:

```bash
npm run dev
```

Open `http://localhost:5173`.

## Main API endpoints

| Method | Endpoint | Access | Purpose |
|---|---|---|---|
| POST | `/api/auth/register/` | Public | Create citizen account |
| POST | `/api/auth/token/` | Public | Obtain JWT access/refresh tokens |
| GET | `/api/auth/me/` | Authenticated | Current account profile |
| GET/POST | `/api/requests/` | Authenticated | List own requests / submit request |
| GET | `/api/requests/{id}/` | Owner or staff | Request details |
| PATCH | `/api/requests/{id}/status/` | Staff only | Update workflow status |
| GET | `/api/requests/{id}/history/` | Owner or staff | Status history |
| GET | `/api/analytics/` | Staff only | Summary counts by status/category |

JWT access tokens are stored in session storage by the demo frontend and cleared on logout. For a high-security production system, consider secure HttpOnly cookie authentication, rate limiting, email verification, audit retention, malware scanning for uploads, and a formal privacy/security review.

## Deploy

### Frontend on Vercel

1. Push this repository to GitHub.
2. In Vercel, import the repository.
3. Set **Root Directory** to `frontend`.
4. Framework preset: **Vite**; Build command: `npm run build`; Output directory: `dist`.
5. Add environment variable `VITE_API_URL=https://YOUR-BACKEND-DOMAIN/api` (no trailing slash after `api`).
6. Deploy.

### Django API + PostgreSQL

1. Create a managed PostgreSQL database and copy its connection URL.
2. Deploy the `backend` directory to Render/Railway as a Python web service. The included `render.yaml` is a starting point for Render.
3. Set `DATABASE_URL`, `DJANGO_SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS` (your Vercel domain), and `CSRF_TRUSTED_ORIGINS`.
4. Set `PYTHON_VERSION` to a supported Python version if required by the host.
5. Run migrations (`python manage.py migrate`) and create a staff account (`python manage.py createsuperuser`).
6. Update Vercel's `VITE_API_URL` to the deployed API URL and redeploy the frontend.

### Uploaded images

Local media storage is suitable for development only. For production, configure durable object storage (for example Cloudinary or S3-compatible storage) before relying on uploaded images; ephemeral app filesystems may be cleared during redeploys.

## Testing

```bash
cd backend
python manage.py test
```

## Evaluation notes

The app includes real database models and permission checks rather than browser-only persistence. Analytics and staff controls require a Django user with `is_staff=True`. The repository does not include real citizen data or hard-coded default administrator credentials. Use fictional data for demonstrations.

## Security controls and traffic scaling

The project includes layered starter controls. They reduce common abuse risks but are not a substitute for a security review before handling real citizen information.

### API rate limiting

Django REST Framework throttling is enabled for anonymous and authenticated traffic. Stricter scoped limits are configured for registration (`5/hour`), login (`10/minute`), and request creation (`20/hour`). General defaults are `60/hour` for anonymous traffic and `600/hour` for authenticated users. Tune these with environment variables (`API_ANON_RATE`, `API_USER_RATE`, `API_REGISTER_RATE`, `API_LOGIN_RATE`, `API_REQUEST_CREATE_RATE`) after observing real traffic.

For production or multiple API instances, configure `REDIS_URL` to a private, authenticated Redis service. Shared Redis means all API instances enforce the same counters. Without it, the development local-memory cache is per-process and limits can be bypassed by distributing requests across instances. The example `infra/nginx/hudumalite.conf` also demonstrates IP-based request/connection limiting at a reverse proxy.

### Application security

- JWT access tokens have a short lifetime; authenticated endpoints require authentication by default.
- Citizens can only see their own requests; staff-only endpoints protect status changes and analytics.
- Registration and login have tighter rate limits; passwords use Django password validators.
- CORS is allow-listed with `CORS_ALLOWED_ORIGINS`; production `ALLOWED_HOSTS` should list only the API host.
- Production mode enables HTTPS redirect (behind a trusted proxy), secure cookies, HSTS, `X-Content-Type-Options`, and clickjacking protection.
- Uploads are limited to 5 MB and accepted image MIME types are checked. For production, add content sniffing/decoding, malware scanning, and private object storage with safe download policy.
- Never commit `.env`, secrets, database credentials, JWTs, or real citizen data. Set `DEBUG=False` and a unique `DJANGO_SECRET_KEY` in deployment.

### Load balancing and scaling

Vercel serves the React frontend; it does not automatically load-balance a separately hosted Django API. Use a platform's managed load balancer when running multiple backend replicas, or adapt `infra/nginx/hudumalite.conf` as a reverse proxy/load balancer in front of at least two private Gunicorn instances. Replace the sample private IP addresses and configure TLS for your own environment; the file is a template, not ready to deploy unchanged.

For horizontal scaling, every API instance must use the same PostgreSQL database and shared Redis cache. Put uploaded images in durable object storage instead of a local instance filesystem. Add health checks, database backups, monitoring, and capacity/load tests before claiming production readiness. A free single-instance deployment is suitable for a demo but is not high availability and does not provide an application-level load balancer by itself.

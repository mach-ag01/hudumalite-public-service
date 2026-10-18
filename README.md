# HudumaLite — Public Service Request System

A full-stack public-service request platform inspired by digital citizen-service portals. HudumaLite enables citizens to submit service requests, attach photos, track progress, and receive status updates while authorized staff manage and resolve reported issues.

Built with **React, Vite, Django REST Framework, and PostgreSQL**, HudumaLite demonstrates full-stack development, REST API integration, authentication, authorization, file uploads, and cloud deployment.

## Live Demo

- **Frontend:** https://hudumalite-public-service-git-main-machag.vercel.app/
- **Backend API:** https://hudumalite-public-service.onrender.com/
- **API Health Check:** https://hudumalite-public-service.onrender.com/api/health/
- **GitHub Repository:** https://github.com/mach-ag01/hudumalite-public-service

The frontend is deployed on Vercel, and the Django API is hosted on Render.

> **Note:** The backend root URL may return HTTP 404 because a homepage is not defined for the API. Use the health-check endpoint to check backend availability. The Render service may take time to wake up if it is on a free instance.
> 
## Assessment Requirements and Implementation

HudumaLite was developed to address the Public Service Request System (Mini eCitizen-style) scenario.

| Assessment requirement | Implementation |
|---|---|
| Citizen registration and login | Django REST Framework authentication with JWT |
| Submit service requests | Request form with category, location, description, and optional image |
| Admin dashboard | Staff-facing request management interface |
| Status tracking | Pending → In Progress → Resolved |
| Basic analytics | Request counts by status, including open and resolved cases |
| Code quality and structure | Separate React frontend and Django backend |
| UI/UX design | Responsive interface for citizen and staff workflows |
| Documentation | README, setup instructions, API reference, and deployment guidance |
| Bonus features | Cloudinary media integration, request history, filtering, and API security controls |

### Suggested Evaluation Workflow

1. Register a citizen account and sign in.
2. Submit a service request with all required fields.
3. Attach an optional image and verify its URL.
4. Open the staff dashboard and locate the submitted request.
5. Update its status from Pending to In Progress, then Resolved.
6. Verify that the citizen can see the latest status.
7. Review the analytics and confirm that the request counts reflect the updated status.

The workflow should be evaluated using test accounts and fictional service-request data. Features and results should be confirmed against the deployed application.
---

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Application Workflow](#application-workflow)
- [Project Structure](#project-structure)
- [Local Development Setup](#local-development-setup)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Authentication and Permissions](#authentication-and-permissions)
- [Image Uploads and Storage](#image-uploads-and-storage)
- [Testing](#testing)
- [Deployment](#deployment)
- [Security Considerations](#security-considerations)
- [Scaling and Production Improvements](#scaling-and-production-improvements)
- [Evaluation Guide](#evaluation-guide)
- [Future Improvements](#future-improvements)
- [Author](#author)

## Project Overview

Public-service issues such as damaged roads, water interruptions, broken streetlights, drainage problems, and waste collection delays need a practical way to be reported and tracked.

HudumaLite provides a digital workflow for reporting these issues and managing their progress.

Citizens can create accounts, submit requests, provide descriptions and locations, attach optional images, and monitor request statuses. Authorized staff can review requests, update their status, and add progress notes. The system also provides request history and staff-facing analytics.

The project demonstrates how a React frontend can communicate with a Django REST API backed by a relational database.

## Key Features

### Citizen Portal

- Citizen registration and JWT authentication.
- Login and authenticated access to personal requests.
- Submission of service requests with a category, location, and description.
- Optional photo attachments.
- Request reference IDs for tracking.
- Request status tracking.
- Viewing request details and available status history.
- Responsive interface for different screen sizes.

### Staff and Administration

- Staff access to request management.
- Request review and status updates.
- Officer notes and status history.
- Search and filtering by status or category.
- Analytics for request totals and workflow status.
- Django administration for authorized administrative operations.

### Request Categories

- Roads
- Water
- Street Lighting
- Waste Collection
- Drainage
- Other

### Backend and Infrastructure

- RESTful API built with Django REST Framework.
- PostgreSQL database support.
- JWT access and refresh tokens.
- Role-based access through authenticated users and staff permissions.
- API pagination and input validation.
- Configurable API rate limits.
- CORS configuration for the deployed frontend.
- Cloudinary integration for uploaded media.
- Environment-based configuration for secrets and deployment settings.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | React |
| Frontend tooling | Vite |
| Backend | Django |
| API | Django REST Framework |
| Authentication | Simple JWT |
| Database | PostgreSQL |
| Image processing | Pillow |
| Image storage | Cloudinary integration |
| Static files | WhiteNoise |
| Application server | Gunicorn |
| Frontend hosting | Vercel |
| Backend hosting | Render |
| Version control | Git and GitHub |

## System Architecture

```text
                   Citizen / Staff
                         |
                         v
                React + Vite Frontend
                     (Vercel)
                         |
                         | HTTPS / REST API
                         v
                 Django REST Framework
                      (Render)
                    /     |      \
                   /      |       \
                  v       v        v
            PostgreSQL  Cloudinary  JWT Auth
              Database  Image Store  & Permissions
```

The frontend handles user interaction and communicates with the backend through HTTP requests. Django validates requests, enforces permissions, and interacts with PostgreSQL. Uploaded images are handled through the configured Cloudinary storage integration.

The frontend and backend are deployed independently, allowing each component to be updated separately.

## Application Workflow

### 1. Citizen submits a report

The citizen logs in, selects a service category, enters a location and description, and optionally attaches a photograph.

### 2. Backend validates the request

Django processes the API request, checks the supplied data and permissions, and stores the request in the database.

### 3. Staff reviews the request

An authorized staff member views the submitted report and updates its progress.

### 4. Status changes are recorded

The request moves through the supported workflow:

`Pending → In Progress → Resolved`

Available status history records changes and associated notes.

### 5. Citizen tracks progress

The citizen returns to the portal to view the request's latest status and available updates.

## Project Structure

The repository follows this general structure. Refer to the actual repository for the complete current file list.

```text
hudumalite-public-service/
├── frontend/
│   ├── src/
│   ├── .env.example
│   └── package.json
├── backend/
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── requests_api/
│   ├── requirements.txt
│   └── .env.example
├── render.yaml
└── README.md
```

- `frontend/` contains the React application.
- `backend/config/` contains Django project configuration.
- `backend/requests_api/` contains the request API implementation.
- `backend/requirements.txt` lists Python dependencies.
- `.env.example` files document required environment-variable names without storing real secrets.
- `render.yaml` provides deployment configuration where supported by the current repository setup.

## Local Development Setup

### Prerequisites

Install the following tools:

- Python version supported by the backend dependencies.
- Node.js 20 or a compatible supported version.
- npm.
- Git.
- PostgreSQL, or access to a PostgreSQL database.

SQLite may be used for local development if the Django settings explicitly support it when `DATABASE_URL` is blank.

### 1. Clone the repository

```bash
git clone https://github.com/mach-ag01/hudumalite-public-service.git
cd hudumalite-public-service
```

### 2. Set up the backend

Open a terminal:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create a local `.env` file using `backend/.env.example` as the reference. Configure the required settings for your local environment.

Apply migrations:

```bash
python manage.py migrate
```

Create an administrative account if needed:

```bash
python manage.py createsuperuser
```

Start Django:

```bash
python manage.py runserver
```

The local API is available at:

`http://127.0.0.1:8000/`

The Django admin interface is available at:

`http://127.0.0.1:8000/admin/`

### 3. Set up the frontend

Open a second terminal from the repository root:

```bash
cd frontend
npm install
```

Create `frontend/.env` using `frontend/.env.example` as a reference.

For local development, configure the API URL to match the actual API base expected by the frontend. For example:

```dotenv
VITE_API_URL=http://127.0.0.1:8000/api
```

Start the frontend:

```bash
npm run dev
```

Open:

`http://localhost:5173/`

**Important:** Confirm the URL conventions in the frontend API client. If it already appends `/api`, do not duplicate that path in `VITE_API_URL`.

## Environment Variables

Environment variables should be configured separately for local development and hosted environments.

| Variable | Purpose |
|---|---|
| `DJANGO_SECRET_KEY` | Django cryptographic signing key |
| `DEBUG` | Enables or disables Django debug mode |
| `DATABASE_URL` | Database connection string |
| `ALLOWED_HOSTS` | Allowed Django request hostnames |
| `CORS_ALLOWED_ORIGINS` | Frontend origins permitted by CORS |
| `CSRF_TRUSTED_ORIGINS` | Trusted origins for CSRF-protected requests |
| `VITE_API_URL` | API base URL used by the Vite frontend |
| `CLOUDINARY_URL` | Cloudinary credentials and cloud configuration |
| `REDIS_URL` | Optional shared Redis connection for caching and rate limiting |
| `SECURE_SSL_REDIRECT` | Controls HTTPS redirection when configured |
| `SECURE_HSTS_SECONDS` | Configures HTTP Strict Transport Security duration |
| `API_ANON_RATE` | General anonymous API request limit |
| `API_USER_RATE` | General authenticated API request limit |
| `API_REGISTER_RATE` | Registration rate limit |
| `API_LOGIN_RATE` | Login rate limit |
| `API_REQUEST_CREATE_RATE` | Request creation rate limit |

The precise requirements depend on the settings and deployment configuration in the current repository.

For production, set `DEBUG=False`, provide a unique `DJANGO_SECRET_KEY`, configure the correct hostnames, and use a valid production database connection.

### Cloudinary configuration

Configure `CLOUDINARY_URL` in the backend hosting provider's environment settings. Its structure is:

```text
cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

Use the real values from your Cloudinary dashboard. Never put actual credentials in the README, source code, screenshots, or Git history.

## API Reference

The following table describes the documented API routes. Verify exact URL patterns and access rules against `backend/config/urls.py` and the corresponding views before relying on them for automated testing.

| Method | Endpoint | Intended access | Purpose |
|---|---|---|---|
| `POST` | `/api/auth/register/` | Public | Register a citizen |
| `POST` | `/api/auth/token/` | Public | Obtain JWT tokens |
| `GET` | `/api/auth/me/` | Authenticated | Retrieve the current user's profile |
| `GET` | `/api/requests/` | Authenticated | List permitted service requests |
| `POST` | `/api/requests/` | Depends on endpoint permissions | Submit a service request |
| `GET` | `/api/requests/{id}/` | Owner or staff | Retrieve request details |
| `PATCH` | `/api/requests/{id}/status/` | Staff only | Update request status |
| `GET` | `/api/requests/{id}/history/` | Owner or staff | Retrieve request history |
| `GET` | `/api/analytics/` | Staff only | Retrieve request analytics |
| `GET` | `/api/health/` | Depends on implementation | Check backend availability |

Replace `{id}` with the relevant request identifier.

### Example: Obtain a JWT token

```http
POST /api/auth/token/
Content-Type: application/json
```

Example request body:

```json
{
  "email": "citizen@example.com",
  "password": "your-password"
}
```

The actual accepted login identifier depends on the configured Django authentication serializer.

### Example: Submit a service request

A request without an image may use JSON, if supported by the endpoint:

```json
{
  "category": "Roads",
  "location": "Example location",
  "description": "A damaged road needs attention."
}
```

For an image upload, the frontend should use `multipart/form-data` and include the supported request fields and image file.

Authenticated requests must include the appropriate access token when required:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Do not share real access tokens in documentation, screenshots, or issue reports.

## Authentication and Permissions

The application uses JSON Web Tokens (JWT) through Django REST Framework and Simple JWT.

The intended permission model includes:

- Public access to citizen registration and token acquisition.
- Authenticated access to protected endpoints.
- Citizens restricted to their own requests.
- Staff-only access to administrative status updates and analytics.
- Validation of submitted request data.

The backend should enforce these rules independently of the frontend. Hiding a button in React is not a substitute for server-side authorization.

JWT access tokens in the demo frontend are stored in session storage and cleared on logout. A production security review should evaluate token handling, session lifetime, refresh-token behavior, and protection against cross-site scripting.

## Image Uploads and Storage

HudumaLite supports optional image attachments on service requests.

Cloudinary is configured as the media-storage provider for the deployed backend. This avoids relying on Render's temporary local filesystem for uploaded images.

The expected flow is:

1. The frontend submits the report and image.
2. Django validates the submitted data and image.
3. The configured storage backend uploads the image to Cloudinary.
4. The API returns the image URL when available.
5. The frontend uses the URL to display the image.

The backend applies upload-size and image-type validation. The implementation should be checked to confirm that the size limit and allowed formats match the current code.

**Persistence verification:** A successful deployment or upload alone does not prove long-term image availability. Test an actual image upload, open the returned URL, and confirm the image remains accessible after a backend restart or redeployment.

For production use, consider stricter content validation, malware scanning, storage quotas, and private access controls where the sensitivity of uploaded material requires them.

## Testing

Run the backend tests from the backend directory:

```bash
python manage.py test
```

Test results should be reviewed before claiming that all tests pass.

### Recommended manual evaluation checklist

- [ ] Register a test citizen.
- [ ] Log in and access the citizen dashboard.
- [ ] Submit a service request with valid fields.
- [ ] Submit a request with an image.
- [ ] Verify that the request appears in the list.
- [ ] Verify that a citizen cannot access another citizen's private request.
- [ ] Log in as authorized staff.
- [ ] Change a request's status and add a note.
- [ ] Verify that the status history is available.
- [ ] Confirm that the citizen sees the updated status.
- [ ] Verify that staff-only analytics are protected.
- [ ] Confirm that an uploaded image URL works after a backend restart or redeployment.

Use fictional accounts and test data for demonstrations.

## Deployment

### Frontend — Vercel

1. Import the GitHub repository into Vercel.
2. Set the project root directory to `frontend`.
3. Select the Vite framework preset.
4. Use `npm run build` as the build command.
5. Use `dist` as the output directory.
6. Set `VITE_API_URL` to the deployed API base URL expected by the frontend.
7. Deploy and verify that the frontend can communicate with the API.

Example:

```dotenv
VITE_API_URL=https://YOUR-BACKEND-DOMAIN/api
```

Ensure that the deployed frontend's origin is included in the backend's CORS configuration.

### Backend — Render

1. Create a Python web service connected to the GitHub repository.
2. Configure the backend directory and build/start commands according to the repository.
3. Configure the production environment variables.
4. Connect the managed PostgreSQL database.
5. Configure Cloudinary for media storage.
6. Run database migrations.
7. Create a staff account securely.
8. Verify the health endpoint and key API routes.
9. Review deployment logs for startup errors and failed requests.

The `render.yaml` file, if present, should be treated as a deployment template and checked against the actual Render service configuration.

### Database

Use a managed PostgreSQL service for deployed application data. Configure connection details through environment variables rather than committing credentials to source control.

Maintain backups and test recovery procedures before using the platform for real public-service records.

## Security Considerations

HudumaLite includes starter security controls intended to reduce common application risks. These controls do not replace a full security review.

### Authentication and authorization

- JWT authentication for protected API requests.
- Staff-only access for administrative functions.
- Server-side permission checks for private request data.
- Password validation through Django's configured password validators.

### Rate limiting

The Django REST Framework settings configure rate limits for anonymous and authenticated requests, with stricter limits intended for registration, login, and request creation.

Example defaults in the current settings include:

- Anonymous requests: `60/hour`
- Authenticated requests: `600/hour`
- Registration: `5/hour`
- Login: `10/minute`
- Request creation: `20/hour`

These limits depend on the configured throttling scopes and view settings. Verify that each scope is applied to the intended endpoint.

For multiple backend instances, configure a shared, authenticated Redis service so rate-limit counters are not isolated to individual application processes.

### Deployment security

- Set `DEBUG=False` in production.
- Use a unique, strong `DJANGO_SECRET_KEY`.
- Restrict `ALLOWED_HOSTS` to the required API hostnames.
- Restrict `CORS_ALLOWED_ORIGINS` to the intended frontend origins.
- Use HTTPS and appropriate secure-cookie settings.
- Keep database and Cloudinary credentials out of source control.
- Validate uploads and monitor unexpected API errors.

Never commit `.env` files, database passwords, JWTs, API secrets, or real citizen data.

## Scaling and Production Improvements

The current deployment is suitable for demonstrating the application. A free or single-instance deployment should not be described as highly available without additional infrastructure.

Potential improvements include:

- Shared Redis caching and rate-limit storage.
- Additional API instances behind a managed load balancer.
- Durable object storage for uploaded media.
- Automated database backups and recovery testing.
- Centralized logging, monitoring, and alerting.
- Automated deployment checks and test execution.
- Load testing and performance optimization.
- Stronger upload validation and malware scanning.
- Security, privacy, and accessibility reviews.

The repository may include example reverse-proxy or load-balancing configuration. Such templates require environment-specific changes and should not be deployed unchanged.

## Evaluation Guide

An assessor can evaluate the project through the following sequence:

1. Open the live frontend.
2. Register or sign in using an authorized test account.
3. Submit a service request and note its reference ID.
4. Verify that the request appears in the citizen dashboard.
5. Sign in as authorized staff and update the request.
6. Check the status history and citizen-facing status.
7. Test image upload and confirm the returned image URL.
8. Review the GitHub repository for the implementation and setup instructions.
9. Run the backend test suite where the required dependencies and database are available.

The repository is intended to demonstrate a working full-stack application with database-backed records and server-side permission checks. Use only test accounts and fictional information during evaluation.

## Future Improvements

Possible future enhancements include:

- Email or SMS notifications for status changes.
- Advanced search and filtering.
- Request assignment to specific departments or officers.
- Map-based issue reporting.
- Service-level agreement tracking.
- More detailed operational reports.
- Improved accessibility and multilingual support.
- Automated deployment and integration tests.

These are proposed enhancements and should not be interpreted as already implemented features.

## Author

**Augustine Mbugua Macharia**

GitHub: https://github.com/mach-ag01

---

*HudumaLite is a demonstration project inspired by digital public-service platforms. It is not an official Kenyan government service and should not be used to submit sensitive personal information or confidential government records.*

# Portfolio Website (FastAPI + React)

Dynamic portfolio platform with:
- Public portfolio pages
- Admin dashboard for CRUD content management
- JWT auth with refresh token rotation
- Image/PDF uploads with validation

## 1. Tech Stack

- Backend: FastAPI, SQLAlchemy, Pydantic, SlowAPI
- Frontend: React 18, Vite, Tailwind CSS, React Query
- Database: SQLite (dev) / PostgreSQL (production)

## 2. Project Structure

```text
backend/
  app/
    api/v1/            # Endpoints
    core/              # Security/dependencies/middleware
    models/            # SQLAlchemy models
    services/          # Upload/sanitize/slug helpers
    main.py            # FastAPI entrypoint
frontend/
  src/
    pages/             # Public + admin pages
    components/        # Shared UI
    services/          # API service layer
docker-compose.yml     # Production container stack
```

## 3. Local Development Run Commands

### Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.main
```

Backend will run at `http://localhost:8000`

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend will run at `http://localhost:5173`

## 4. Admin Login Bootstrap

Create first admin user:

```powershell
cd backend
python create_admin.py
```

Then login at:
- `http://localhost:5173/admin/login`

## 5. Production Run Commands (Docker)

### Step 1: Prepare env file

```powershell
Copy-Item backend/.env.production.example backend/.env.production
```

Edit `backend/.env.production` and set a strong `SECRET_KEY`.

### Step 2: Start production stack

```powershell
docker compose up -d --build
```

Services:
- Frontend: `http://localhost`
- Backend API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

### Step 3: Stop production stack

```powershell
docker compose down
```

## 6. Production Run Commands (Without Docker)

### Backend

```powershell
cd backend
.\venv\Scripts\Activate.ps1
setx ENVIRONMENT production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
```

### Frontend

```powershell
cd frontend
npm run build
npm run preview -- --host 0.0.0.0 --port 4173
```

## 7. API Notes

- Public endpoints: `/api/v1/personal`, `/api/v1/projects`, etc.
- Auth endpoints:
  - `POST /api/v1/auth/login`
  - `POST /api/v1/auth/refresh`
  - `POST /api/v1/auth/logout`
  - `POST /api/v1/auth/register` (admin only)
  - `GET /api/v1/auth/me`
- Health:
  - `GET /health`
  - `GET /api/v1/health`

## 8. Verification Commands

### Backend syntax check

```powershell
python -m compileall backend/app
```

### Frontend production build

```powershell
cd frontend
npm run build
```

## 9. CI/CD (GitHub Actions)

- Frontend auto-deploys to GitHub Pages on push to `main` when files in `frontend/**` change.
- Backend auto-validates and triggers deploy on push to `main` when files in `backend/**` change.

### Required GitHub repository configuration

1. Enable GitHub Pages source:
   - `Settings -> Pages -> Source: GitHub Actions`
2. Add repository variable:
   - `Settings -> Secrets and variables -> Actions -> Variables`
   - `VITE_API_BASE_URL=https://your-backend-domain`
3. Add repository secret for backend deploy hook:
   - `Settings -> Secrets and variables -> Actions -> Secrets`
   - `BACKEND_DEPLOY_HOOK_URL=<your-backend-provider-deploy-hook>`
   - For Render, you can use `RENDER_DEPLOY_HOOK_URL` instead.

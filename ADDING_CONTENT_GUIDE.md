# Step-by-Step Guide: Adding Content to Portfolio Website

This guide explains how to add content in the backend so it's automatically reflected in the frontend.

## 🎯 Overview

Your portfolio uses a **Full Stack Architecture**:
- **Backend (FastAPI)**: Stores and manages data in SQLite database
- **Frontend (React)**: Fetches and displays data via API calls
- **Communication**: REST API endpoints with standardized JSON responses

---

## 📝 Step-by-Step Process

### Example: Adding a New Certification

Let's walk through adding a certification as an example. The same process applies to all content types (projects, articles, education, experience, etc.).

---

## Step 1: Start Both Servers

Before you can add content, ensure both backend and frontend are running.

### Backend Server

```powershell
# Open terminal 1
cd d:\Portfolio_Fastapi_antigravity_fully_dynamic\backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start backend server
python -m app.main
```

✅ Backend running at: `http://localhost:8000`
📖 API Documentation: `http://localhost:8000/docs`

### Frontend Server

```powershell
# Open terminal 2 (new terminal)
cd d:\Portfolio_Fastapi_antigravity_fully_dynamic\frontend

# Start frontend server
npm run dev
```

✅ Frontend running at: `http://localhost:5173`

---

## Step 2: Authenticate as Admin

You need admin access to create/edit content.

### Option A: Using the Frontend (Recommended)

1. Navigate to `http://localhost:5173/admin/login`
2. Enter your admin credentials:
   - Email: `admin@example.com`
   - Password: Your admin password

### Option B: Using API Documentation

1. Go to `http://localhost:8000/docs`
2. Find `/api/v1/auth/login` endpoint
3. Click "Try it out"
4. Enter credentials in JSON format:
```json
{
  "email": "admin@example.com",
  "password": "your_password"
}
```
5. Copy the `access_token` from the response

---

## Step 3: Add Content via API

You have two main approaches to add content:

### Approach A: Using FastAPI Docs (Easiest for Testing) ✨

1. **Navigate to API Documentation**
   - Open `http://localhost:8000/docs`

2. **Locate the Endpoint**
   - Find **POST /api/v1/certifications** (or relevant endpoint)
   - Click to expand it

3. **Authorize**
   - Click the 🔒 lock icon at the top right
   - Enter your access token: `Bearer YOUR_ACCESS_TOKEN`
   - Click "Authorize"

4. **Try the Endpoint**
   - Click "Try it out"
   - Fill in the request body:

```json
{
  "name": "AWS Solutions Architect",
  "issuer": "Amazon Web Services",
  "issue_month_year": "2024-01",
  "cred_id": "ABC123XYZ",
  "cred_url": "https://aws.amazon.com/verification/ABC123XYZ",
  "description": "<p>Professional certification in AWS cloud architecture</p>"
}
```

5. **Execute**
   - Click "Execute"
   - Check the response (should show `"success": true`)

6. **Upload Image (Optional)**
   - Find **POST /api/v1/certifications/{cert_id}/upload-image**
   - Use the `id` from the previous response
   - Upload your certificate image

---

### Approach B: Using curl/PowerShell (For Automation)

```powershell
# Step 1: Login and get token
$loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"email":"admin@example.com","password":"your_password"}'

$token = $loginResponse.data.access_token

# Step 2: Create certification
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$certData = @{
    name = "AWS Solutions Architect"
    issuer = "Amazon Web Services"
    issue_month_year = "2024-01"
    cred_id = "ABC123XYZ"
    cred_url = "https://aws.amazon.com/verification/ABC123XYZ"
    description = "<p>Professional certification in AWS cloud architecture</p>"
} | ConvertTo-Json

$certResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/certifications" `
    -Method POST `
    -Headers $headers `
    -Body $certData

Write-Host "Created certification with ID: $($certResponse.data.id)"
```

---

### Approach C: Building a Frontend Admin Form (Production Way)

This is how you'd typically do it in production (you'll need to build the UI):

**Frontend React Example:**

```jsx
// In your Admin Certifications page
import axios from '@/lib/axios';

const createCertification = async (formData) => {
  try {
    const response = await axios.post('/api/v1/certifications', {
      name: formData.name,
      issuer: formData.issuer,
      issue_month_year: formData.issueDate,
      cred_id: formData.credId,
      cred_url: formData.credUrl,
      description: formData.description
    });
    
    console.log('Created:', response.data);
    // Handle success (show toast, redirect, etc.)
    
  } catch (error) {
    console.error('Error:', error);
    // Handle error
  }
};
```

---

## Step 4: Verify Data in Backend

### Check Database Directly

```powershell
# In backend directory
cd d:\Portfolio_Fastapi_antigravity_fully_dynamic\backend

# Open SQLite database
sqlite3 portfolio.db

# Query certifications
SELECT * FROM certifications;

# Exit
.quit
```

### Check via API

```powershell
# Get all certifications (public endpoint, no auth needed)
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/certifications"
```

---

## Step 5: Frontend Automatically Displays the Data

Once you've added data to the backend, the frontend will automatically fetch and display it when you visit the relevant page.

### How Frontend Fetches Data

**Example: Certifications List Component**

```jsx
// Frontend component (when you build it)
import { useQuery } from '@tanstack/react-query';
import axios from '@/lib/axios';

const CertificationsList = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['certifications'],
    queryFn: async () => {
      const response = await axios.get('/api/v1/certifications');
      return response.data; // Axios interceptor extracts .data.data
    }
  });

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      {data?.map(cert => (
        <div key={cert.id}>
          <h3>{cert.name}</h3>
          <p>{cert.issuer} - {cert.issue_month_year}</p>
          {cert.image && <img src={`http://localhost:8000${cert.image}`} />}
        </div>
      ))}
    </div>
  );
};
```

### What Happens Behind the Scenes

1. **Component Mounts** → Triggers API call
2. **Axios Request** → `GET /api/v1/certifications`
3. **Backend Query** → Fetches from SQLite database
4. **Response** → Returns JSON with certification data
5. **Frontend Renders** → Displays the data in UI

---

## 🗂️ Content Types & Endpoints

Here's a quick reference for all content types:

| Content Type | Public Endpoint (GET) | Admin Create (POST) | Admin Update (PATCH) | Admin Delete (DELETE) |
|--------------|----------------------|---------------------|---------------------|----------------------|
| **Personal Info** | `/api/v1/personal` | `/api/v1/personal` | `/api/v1/personal` | N/A |
| **Education** | `/api/v1/education` | `/api/v1/education` | `/api/v1/education/{id}` | `/api/v1/education/{id}` |
| **Experience** | `/api/v1/experience` | `/api/v1/experience` | `/api/v1/experience/{id}` | `/api/v1/experience/{id}` |
| **Skills** | `/api/v1/skills` | `/api/v1/skills` | `/api/v1/skills/{id}` | `/api/v1/skills/{id}` |
| **Projects** | `/api/v1/projects` | `/api/v1/projects` | `/api/v1/projects/{id}` | `/api/v1/projects/{id}` |
| **Articles** | `/api/v1/articles` | `/api/v1/articles` | `/api/v1/articles/{id}` | `/api/v1/articles/{id}` |
| **Certifications** | `/api/v1/certifications` | `/api/v1/certifications` | `/api/v1/certifications/{id}` | `/api/v1/certifications/{id}` |
| **Extracurricular** | `/api/v1/extracurricular` | `/api/v1/extracurricular` | `/api/v1/extracurricular/{id}` | `/api/v1/extracurricular/{id}` |
| **Resource Papers** | `/api/v1/resource-papers` | `/api/v1/resource-papers` | `/api/v1/resource-papers/{id}` | `/api/v1/resource-papers/{id}` |

---

## 📸 Adding Images/Files

Most content types support file uploads. Here's how:

### Step 1: Create the Content First

```json
POST /api/v1/certifications
{
  "name": "My Certification",
  "issuer": "Tech Institute",
  "issue_month_year": "2024-01"
}
```

### Step 2: Upload Image/File

```powershell
# Using PowerShell
$headers = @{
    "Authorization" = "Bearer YOUR_TOKEN"
}

$form = @{
    file = Get-Item -Path "C:\path\to\certificate.jpg"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/certifications/{cert_id}/upload-image" `
    -Method POST `
    -Headers $headers `
    -Form $form
```

### Uploaded Files Location

Files are stored in: `d:\Portfolio_Fastapi_antigravity_fully_dynamic\backend\uploads\`

### Frontend Access

```jsx
// Images are served by backend
<img src={`http://localhost:8000${certification.image}`} alt={certification.name} />
```

---

## 🔄 Complete Workflow Example

Let's add a complete education entry:

### 1. Create Education Entry

```json
POST /api/v1/education
{
  "institution": "Stanford University",
  "degree": "Master of Science",
  "field": "Computer Science",
  "location": "Stanford, CA",
  "grade": "3.9 GPA",
  "start_month_year": "2020-09",
  "end_month_year": "2022-06",
  "description": "<p>Focused on Machine Learning and AI</p>"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Education created successfully",
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "institution": "Stanford University",
    ...
  }
}
```

### 2. Upload Institution Logo

```powershell
POST /api/v1/education/{id}/upload-logo
# Upload stanford_logo.png
```

### 3. View on Frontend

Navigate to `http://localhost:5173/education` (once built)

The education entry appears automatically! ✨

---

## 🛠️ Troubleshooting

### Issue: "401 Unauthorized"

**Solution:** Your token expired or is invalid
- Login again to get a fresh token
- Check if you included `Authorization: Bearer TOKEN` header

### Issue: "404 Not Found"

**Solution:** Wrong endpoint URL
- Check the API documentation at `http://localhost:8000/docs`
- Ensure backend server is running

### Issue: "422 Unprocessable Entity"

**Solution:** Invalid data format
- Check required fields in the model
- Verify date format (should be `YYYY-MM` for month-year fields)
- Ensure JSON is properly formatted

### Issue: Frontend Not Showing Data

**Solutions:**
1. **Check if backend has data:**
   ```powershell
   Invoke-RestMethod -Uri "http://localhost:8000/api/v1/certifications"
   ```

2. **Check browser console** for errors

3. **Verify API URL** in frontend config

4. **Check CORS settings** in backend

5. **Hard refresh** browser (Ctrl + F5)

---

## 📊 Data Flow Diagram

```
┌─────────────────┐
│   Admin User    │
└────────┬────────┘
         │ 1. Login
         ▼
┌─────────────────┐
│  POST /auth/    │
│     login       │──────► Get JWT Token
└────────┬────────┘
         │ 2. Create Content
         ▼
┌─────────────────┐
│POST /certifi-   │
│   cations       │──────► Save to Database
└────────┬────────┘        (portfolio.db)
         │
         │ 3. Upload Image (Optional)
         ▼
┌─────────────────┐
│POST /certifi-   │
│cations/{id}/    │──────► Save to uploads/
│upload-image     │
└─────────────────┘
         │
         │ 4. Frontend Fetches
         ▼
┌─────────────────┐
│GET /certifi-    │
│    cations      │◄────── React Component
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Display in     │
│   Frontend UI   │
└─────────────────┘
```

---

## 🎯 Quick Reference Commands

### Backend Operations

```powershell
# Start backend
cd d:\Portfolio_Fastapi_antigravity_fully_dynamic\backend
.\venv\Scripts\Activate.ps1
python -m app.main

# View database
sqlite3 portfolio.db
.tables
SELECT * FROM certifications;
.quit

# Create admin user
python create_admin.py
```

### Frontend Operations

```powershell
# Start frontend
cd d:\Portfolio_Fastapi_antigravity_fully_dynamic\frontend
npm run dev

# Install dependencies (if needed)
npm install
```

### API Testing

```powershell
# Get all certifications (public)
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/certifications"

# Health check
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

---

## 📚 Next Steps

Once you're comfortable adding content via API:

1. **Build Admin Dashboard UI** - Create forms in React for easier content management
2. **Build Public Pages** - Display content on public-facing portfolio pages
3. **Add Validation** - Implement form validation on frontend
4. **Add Loading States** - Show spinners while data loads
5. **Add Error Handling** - Display user-friendly error messages

---

## 💡 Pro Tips

1. **Use API Documentation** - `http://localhost:8000/docs` is your best friend for testing
2. **Check Response Format** - All responses follow: `{success, message, data}`
3. **Soft Deletes** - Deleted items aren't removed, just marked `is_deleted=true`
4. **Slugs Auto-Generated** - Projects/Articles get automatic URL-friendly slugs
5. **Image Optimization** - Backend auto-compresses images to WebP
6. **Rate Limiting** - Max 100 requests per minute (won't affect normal use)

---

## 🎓 Summary

**The Complete Flow:**

1. ✅ Start backend + frontend servers
2. 🔐 Login as admin to get JWT token
3. ➕ Create content via POST endpoint (with auth)
4. 📸 Upload images/files (optional)
5. ✨ Frontend automatically fetches and displays data

**Key Concept:** 
> Backend is the **single source of truth**. Frontend just displays what backend provides. Add to backend → Automatically appears in frontend!

---

## 📞 Need Help?

- **API Docs:** `http://localhost:8000/docs`
- **View Models:** Check `backend/app/models/`
- **View Endpoints:** Check `backend/app/api/v1/`
- **Database:** `backend/portfolio.db`

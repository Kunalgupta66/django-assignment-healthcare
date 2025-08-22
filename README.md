# 🏥 Healthcare Management API

A Django REST Framework (DRF) based backend system for managing **patients, doctors, and their mappings**.  
Implements **JWT authentication**, role-based access, and PostgreSQL as the database.  

---

## 🚀 Features
- **Authentication** (Register, Login, Refresh Token)  
- **Patient Management** (CRUD, linked to logged-in user)  
- **Doctor Management** (CRUD, global access)  
- **Patient-Doctor Mappings** (assign patients to doctors, view mappings)  
- **Permissions**: Only authenticated users can create/view patients  

---

## 🛠 Tech Stack
- Python 3.11  
- Django 5 + Django REST Framework  
- PostgreSQL  
- JWT Authentication (`djangorestframework-simplejwt`)  

---

## ⚙️ Setup Instructions
1. Clone the repo & create virtual environment:
   ```bash
   git clone <repo_url>
   cd Django-Assignment
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Setup PostgreSQL and create a database:
   ```sql
   CREATE DATABASE healthcare_db;
   CREATE USER postgres WITH PASSWORD <your_password_here>;
   GRANT ALL PRIVILEGES ON DATABASE healthcare_db TO postgres;
   ```

4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Start the server:
   ```bash
   python manage.py runserver
   ```

---

## 🔑 API Endpoints

### Auth
- `POST /api/auth/register/` → Register user  
- `POST /api/auth/login/` → Login & get JWT tokens  
- `POST /api/auth/token/refresh/` → Refresh token  

### Patients
- `POST /api/patients/` → Add patient  
- `GET /api/patients/` → List user’s patients  
- `GET /api/patients/<id>/` → Get patient details  
- `PUT /api/patients/<id>/` → Update patient  
- `DELETE /api/patients/<id>/` → Delete patient  

### Doctors
- `POST /api/doctors/` → Add doctor  
- `GET /api/doctors/` → List doctors  
- `GET /api/doctors/<id>/` → Get doctor details  
- `PUT /api/doctors/<id>/` → Update doctor  
- `DELETE /api/doctors/<id>/` → Delete doctor  

### Mappings
- `POST /api/mappings/` → Map patient to doctor  
- `GET /api/mappings/` → List all mappings  
- `GET /api/mappings/<id>/` → Get mapping details  
- `DELETE /api/mappings/<id>/` → Delete mapping  
- `GET /api/mappings/<patient_id>/` → Get all doctors for a patient  

---

## 🧪 Testing with Postman
- Use JWT `Authorization: Bearer <access_token>` for all endpoints.  
- Example `POST /api/patients/` body:
  ```json
  {
    "name": "Ravi Kumar",
    "age": 34,
    "gender": "male"
  }
  ```

---
⚠️ Note: Create a `.env` file with your PostgreSQL username/password before running.


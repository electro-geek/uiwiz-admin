# UIWiz Admin

Admin panel for **UIWiz** and **uiwiz-backend**. Django backend + Django templates frontend, using the **same database** as uiwiz-backend.

## Features

- **Dashboard**: List all users with last login and Gemini API keys (from `auth_user` and `api_userprofile`).
- **Django Admin**: Full admin at `/admin/` for User and UserProfile (same DB, read-only friendly).

## Setup

1. **Same DB as uiwiz-backend**

   Copy `config.properties.example` to `config.properties` and set the same database credentials you use in **uiwiz-backend** (or set env vars `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`).

2. **Virtualenv and install**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # or: venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **Create a staff user** (admin panel uses Django auth; no migrations are run on the shared DB)

   Create a superuser in this project so you can log in to the admin and dashboard:

   ```bash
   python manage.py createsuperuser
   ```

4. **Run**

   ```bash
   python manage.py runserver
   ```

   - Dashboard: http://localhost:8000/
   - Django Admin: http://localhost:8000/admin/

## Notes

- The dashboard app uses **unmanaged** models that point to the existing `api_userprofile` table; it does not create or alter tables in the shared database.
- You must create at least one Django superuser (or staff user) in this project to log in; that user is stored in the same `auth_user` table used by uiwiz-backend.

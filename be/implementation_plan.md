# Render Deployment Plan for Django backend

## Changes needed

1. settings.py — make SECRET_KEY, DEBUG, ALLOWED_HOSTS env-driven; add DATABASE_URL support via dj-database-url
2. requirements.txt — add dj-database-url
3. build.sh — Render build script (pip install, collectstatic, migrate)
4. .env.example — document new required env vars
5. .gitignore — ensure .env and env/ are excluded

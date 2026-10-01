# LEAPNITPY

A Django learning and mentorship platform for JEE/NEET students. It includes Google sign-in, study resources, timed tests, results, and a leaderboard. The production site is hosted on Hostinger and has been tested with hundreds of students (project-owner reported).

## Stack and architecture

- Django 4.2, django-allauth (Google OAuth), PostgreSQL, Gunicorn, Nginx
- `website/` contains models, views, forms, migrations, and routes
- `templates/` and `assets/` contain the server-rendered interface
- `LeapWeb/settings.py` reads deployment configuration from environment variables
- `deploy_leap.sh` is the current Hostinger deployment helper; review its server paths and permissions before running it on another host

## Local setup

1. Create a Python virtual environment outside Git tracking and install `requirements.txt`.
2. Copy `.env.example` to `.env`. Set a local PostgreSQL database's `DB_NAME`, `DB_USER`, and `DB_PASSWORD`, and use `DJANGO_DEBUG=True` for local development.
3. Run `python manage.py migrate` and `python manage.py runserver`.
4. Google sign-in requires a Google OAuth web client with the correct authorized redirect URI. Put its client ID and client secret in the local `.env` or Hostinger environment settings, never in source code.

Production must set a persistent, randomly generated `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS`, the database variables, and the Google OAuth variables. HTTPS is required in production; secure cookies and HTTPS redirection default to on when debug is off. Verify that the reverse proxy strips untrusted `X-Forwarded-Proto` headers before deployment.

## Security notes

- `.env`, local environments, generated static files, and logs are ignored for new additions. Some machine-generated files are still tracked in the initial commit; do not delete the virtual environment on the live Hostinger server without first creating a replacement.
- The Google client ID is an identifier, not a password. The Google client secret, Django secret key, database password, and email password must remain in private environment configuration.
- If a real credential was ever published, removing it from the current code is insufficient: rotate or revoke it at the provider, then update Hostinger. Git history and forks may retain old values.
- Never commit student records, database dumps, or production logs. Use synthetic examples for public demonstrations.

## Verification

Run `python manage.py check --deploy` with production-like environment variables and `python manage.py test` before deployment. These checks do not replace a staging smoke test of Google login, test submission, and the leaderboard.

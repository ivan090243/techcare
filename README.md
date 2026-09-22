# TechCare Home Services

Production-ready Django web application for **TechCare Home Services** — a home-service computer repair and maintenance business.

## Features

- **Public site**: Home, Services, Pricing (TBA), Booking, Gallery, Testimonials, FAQ, Contact
- **Booking system**: Guest bookings with email notifications to admin
- **Admin dashboard**: Manage bookings, services, customers; search, filter, Excel export
- **Design**: Bootstrap 5, dark blue glassmorphism, fully responsive
- **Security**: CSRF protection, input validation, staff-only dashboard
- **Deployment-ready**: SQLite (dev), PostgreSQL via `DATABASE_URL` (Railway)

## Quick Start (Development)

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run migrations and seed data
python manage.py migrate
python manage.py seed_data
python manage.py create_admin

# Start server
python manage.py runserver
```

- **Website**: http://127.0.0.1:8000/
- **Admin dashboard**: http://127.0.0.1:8000/dashboard/
- **Django admin**: http://127.0.0.1:8000/admin/

Default admin credentials (change in production):
- Username: `admin`
- Password: `admin12345`

## Project Structure

```
techcare/
├── config/settings/     # base, development, production
├── core/                # Home, contact, pricing, shared models
├── services/            # Service catalog
├── bookings/            # Booking system & email notifications
├── content/             # Gallery, testimonials, FAQ
├── dashboard/           # Custom admin dashboard
├── templates/           # HTML templates
└── static/              # CSS & JS
```

## Railway Deployment

1. Create a new Railway project and add **PostgreSQL**
2. Set environment variables:
   - `DJANGO_SETTINGS_MODULE=config.settings.production`
   - `SECRET_KEY` — long random string
   - `DATABASE_URL` — auto-set by Railway PostgreSQL
   - `ALLOWED_HOSTS` — your Railway domain
   - `CSRF_TRUSTED_ORIGINS` — `https://your-domain.up.railway.app`
   - `ADMIN_EMAIL`, `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
3. Deploy — migrations run via `railway.toml` start command
4. Run once: `python manage.py seed_data && python manage.py create_admin`

## Future-Ready Architecture

Models include extensible fields for:
- Walk-in & pick-up/delivery service types
- Customer & technician accounts
- Inventory, payments, SMS, multi-branch support

## License

Proprietary — TechCare Home Services

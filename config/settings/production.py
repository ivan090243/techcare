"""Production settings for Railway and Vercel deployments."""

from .base import *  # noqa: F403

DEBUG = False
# The base setting provides a development fallback so a missing Vercel variable
# does not prevent the serverless function from importing. Set SECRET_KEY in Vercel.
SECRET_KEY = env("SECRET_KEY", default=SECRET_KEY)  # noqa: F405
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])  # noqa: F405

if not ALLOWED_HOSTS:
    railway_domain = env("RAILWAY_PUBLIC_DOMAIN", default="")  # noqa: F405
    if railway_domain:
        ALLOWED_HOSTS = [railway_domain]

vercel_domains = [  # noqa: F405
    env("VERCEL_URL", default=""),
    env("VERCEL_PROJECT_PRODUCTION_URL", default=""),
]
ALLOWED_HOSTS.extend(domain for domain in vercel_domains if domain and domain not in ALLOWED_HOSTS)

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])  # noqa: F405
if not CSRF_TRUSTED_ORIGINS and ALLOWED_HOSTS:
    CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)  # noqa: F405
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)  # noqa: F405
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

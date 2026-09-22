import os
import shutil
import tempfile
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

# Vercel's deployed project directory is read-only. Keep PostgreSQL as the
# production database when configured, and use a writable per-instance copy
# of the build database only as a serverless fallback.
if not os.environ.get("DATABASE_URL"):
	project_root = Path(__file__).resolve().parent.parent
	source_database = project_root / "db.sqlite3"
	runtime_database = Path(tempfile.gettempdir()) / "techcare.sqlite3"
	if source_database.exists() and not runtime_database.exists():
		shutil.copy2(source_database, runtime_database)
	os.environ["DATABASE_URL"] = f"sqlite:///{runtime_database}"

from config.wsgi import application


app = application
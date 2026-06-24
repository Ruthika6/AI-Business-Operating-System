import os
from dotenv import load_dotenv

load_dotenv()

# Gemini configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Database configuration
DATABASE_URL = os.environ.get("DATABASE_URL", "")

if not DATABASE_URL:
    # If running on Vercel or in a read-only directory, use /tmp/flowzint.db for SQLite
    is_vercel = os.environ.get("VERCEL") == "1" or "VERCEL" in os.environ
    
    # Check write access to the current directory
    try:
        test_file = "test_write.tmp"
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        is_writable = True
    except Exception:
        is_writable = False

    if is_vercel or not is_writable:
        # Use system temp directory or /tmp
        import tempfile
        db_path = os.path.join(tempfile.gettempdir(), "flowzint.db")
        DATABASE_URL = f"sqlite:///{db_path}"
    else:
        DATABASE_URL = "sqlite:///flowzint.db"

# Format DATABASE_URL for SQLAlchemy if it uses postgres:// (Heroku/Render standard)
# SQLAlchemy 1.4+ requires postgresql:// instead of postgres://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

PORT = int(os.environ.get("PORT", 8000))
ENV = os.environ.get("ENV", "development")

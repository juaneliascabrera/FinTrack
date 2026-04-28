import sys
from pathlib import Path

# Add the backend app to the path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "fintrack-backend"))

from app.app import app  # noqa: E402

# Vercel expects the FastAPI instance to be named 'app'
# and it should be importable from the entrypoint

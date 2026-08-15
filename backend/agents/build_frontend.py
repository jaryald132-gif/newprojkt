# backend/agents/build_frontend.py
import os
from pathlib import Path

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
FRONTEND_DIR.mkdir(parents=True, exist_ok=True)
print(f"Frontend directory ready at: {FRONTEND_DIR}")

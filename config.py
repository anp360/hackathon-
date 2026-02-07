# Configuration for Crisis Management AI System

import os
from datetime import datetime

# Gemini AI Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-api-key-here")
GEMINI_MODEL = "gemini-pro"  # Changed from gemini-1.5-flash to gemini-pro

# Supported locations
LOCATIONS = ["Tambaram", "Velachery", "Perungudi", "Saidapet", "Other"]

# Need categories
NEED_CATEGORIES = ["food", "water", "medical", "shelter", "rescue", "clothing", "unknown"]

# Urgency levels
URGENCY_LEVELS = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]

# Time-sensitive needs (hours of day when these are more critical)
TIME_SENSITIVE_NEEDS = {
    "shelter": {
        "critical_hours": list(range(18, 24)) + list(range(0, 6)),  # 6 PM to 6 AM
        "reason": "Nighttime exposure is life-threatening"
    },
    "medical": {
        "critical_hours": list(range(0, 24)),  # Always critical
        "reason": "Medical emergencies require immediate attention"
    },
    "food": {
        "critical_hours": list(range(6, 9)) + list(range(12, 14)) + list(range(18, 21)),  # Meal times
        "reason": "Peak meal times for vulnerable populations"
    }
}

# Database file
DB_FILE = "data/messages_db.json"

# Flask Configuration
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True

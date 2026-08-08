import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

TARIFFS = {
    "free": {"name": "Free", "price": 0, "workouts_per_month": 3},
    "lite": {"name": "Lite", "price": 99, "workouts_per_month": 8},
    "pro": {"name": "Pro", "price": 249, "workouts_per_month": 999},
    "elite": {"name": "Elite", "price": 499, "workouts_per_month": 999},
}

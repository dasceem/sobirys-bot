import sqlite3
import json
from datetime import datetime

DB_PATH = "sobirys.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            tariff TEXT DEFAULT 'free',
            created_at TEXT,
            questionnaire TEXT,
            current_program TEXT,
            workouts_done INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 0,
            last_workout TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS workouts_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            program_name TEXT,
            workout_name TEXT,
            duration_min INTEGER,
            completed_at TEXT,
            exercises_done INTEGER
        )
    """)
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row

def add_user(user_id, username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute("INSERT OR IGNORE INTO users (user_id, username, created_at) VALUES (?, ?, ?)",
              (user_id, username, now))
    conn.commit()
    conn.close()

def save_questionnaire(user_id, data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET questionnaire = ? WHERE user_id = ?",
              (json.dumps(data, ensure_ascii=False), user_id))
    conn.commit()
    conn.close()

def get_questionnaire(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT questionnaire FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row and row[0]:
        return json.loads(row[0])
    return {}

def set_program(user_id, program_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET current_program = ? WHERE user_id = ?",
              (program_name, user_id))
    conn.commit()
    conn.close()

def get_program(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT current_program FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def log_workout(user_id, program_name, workout_name, duration, exercises_done):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute("""
        INSERT INTO workouts_log (user_id, program_name, workout_name, duration_min, completed_at, exercises_done)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, program_name, workout_name, duration, now, exercises_done))
    c.execute("SELECT workouts_done, streak, last_workout FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    if row:
        workouts_done = row[0] + 1
        last = row[2]
        streak = row[1]
        if last:
            last_date = datetime.fromisoformat(last).date()
            today = datetime.now().date()
            diff = (today - last_date).days
            if diff == 1:
                streak += 1
            elif diff > 1:
                streak = 1
        else:
            streak = 1
        c.execute("UPDATE users SET workouts_done = ?, streak = ?, last_workout = ? WHERE user_id = ?",
                  (workouts_done, streak, now, user_id))
    conn.commit()
    conn.close()

def get_stats(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT workouts_done, streak FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return {"workouts_done": row[0] if row else 0, "streak": row[1] if row else 0}

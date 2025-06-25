import sqlite3
from datetime import datetime

# Connect to (or create) the database
conn = sqlite3.connect("planner.db")
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        time TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

# Add a new task
def add_task(title, time):
    cursor.execute("INSERT INTO tasks (title, time) VALUES (?, ?)", (title, time))
    conn.commit()

# Get tasks scheduled for today
def get_tasks_for_today():
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Create a new connection and cursor locally in the thread
    conn = sqlite3.connect("planner.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE DATE(time) = ?", (today,))
    results = cursor.fetchall()

    conn.close()
    return results


# Delete a task by ID
def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

# Update a task
def update_task(task_id, new_title, new_time):
    cursor.execute("UPDATE tasks SET title = ?, time = ? WHERE id = ?", (new_title, new_time, task_id))
    conn.commit()

# Close connection (optional, can be used in main app exit)
def close_connection():
    conn.close()

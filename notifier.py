import threading
import time
from datetime import datetime
from plyer import notification
from database import get_tasks_for_today

notified_tasks = set()

def check_for_notifications():
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        tasks = get_tasks_for_today()

        for task in tasks:
            task_id, title, time_str, _ = task
            task_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")

            if task_time == now and task_id not in notified_tasks:
                # Show desktop notification
                notification.notify(
                    title="📝 Task Reminder",
                    message=f"{title} at {task_time}",
                    timeout=10  # seconds
                )
                notified_tasks.add(task_id)

        time.sleep(30)  # Check every 30 seconds

def start_notification_thread():
    thread = threading.Thread(target=check_for_notifications, daemon=True)
    thread.start()

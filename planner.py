import tkinter as tk
from tkinter import messagebox, simpledialog
from database import add_task, get_tasks_for_today, delete_task
from datetime import datetime
from notifier import start_notification_thread

# --- Main Application Class ---
class PlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Daily Planner")
        self.root.geometry("500x400")
        
        self.task_frame = tk.Frame(root)
        self.task_frame.pack(pady=10, fill="both", expand=True)
        
        # Title
        tk.Label(root, text="Today's Tasks", font=("Arial", 16)).pack()

        # Task list
        self.task_listbox = tk.Listbox(self.task_frame, font=("Arial", 12), height=10)
        self.task_listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.task_frame, orient="vertical", command=self.task_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Task", command=self.add_task_dialog).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete Task", command=self.delete_selected_task).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.load_tasks).pack(side="left", padx=5)

        self.load_tasks()

    # Load today's tasks from the DB
    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = get_tasks_for_today()
        for task in tasks:
            task_id, title, time, _ = task
            time_str = datetime.strptime(time, "%Y-%m-%d %H:%M").strftime("%I:%M %p")
            self.task_listbox.insert(tk.END, f"{task_id}. {title} at {time_str}")

    # Add task via dialog
    def add_task_dialog(self):
        title = simpledialog.askstring("Task Title", "Enter task title:")
        time_input = simpledialog.askstring("Task Time", "Enter time (YYYY-MM-DD HH:MM):")
        try:
            datetime.strptime(time_input, "%Y-%m-%d %H:%M")
            add_task(title, time_input)
            self.load_tasks()
        except:
            messagebox.showerror("Invalid Time Format", "Use format: YYYY-MM-DD HH:MM")

    # Delete selected task
    def delete_selected_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a task to delete.")
            return
        task_text = self.task_listbox.get(selection[0])
        task_id = int(task_text.split(".")[0])
        delete_task(task_id)
        self.load_tasks()

start_notification_thread()
# --- Run the App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PlannerApp(root)
    root.mainloop()

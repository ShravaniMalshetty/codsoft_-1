import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List Manager")
        self.root.geometry("600x500")

        # Data storage
        self.tasks = []
        self.load_tasks()

        # Main container
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Task input area
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=0, column=0, pady=10, sticky=(tk.W, tk.E))

        self.task_var = tk.StringVar()
        self.priority_var = tk.StringVar(value="Medium")

        ttk.Label(input_frame, text="Task:").grid(row=0, column=0, padx=5)
        ttk.Entry(input_frame, textvariable=self.task_var, width=40).grid(
            row=0, column=1, padx=5
        )

        ttk.Label(input_frame, text="Priority:").grid(row=0, column=2, padx=5)
        priority_combo = ttk.Combobox(
            input_frame,
            textvariable=self.priority_var,
            values=["High", "Medium", "Low"],
            width=8,
        )
        priority_combo.grid(row=0, column=3, padx=5)

        ttk.Button(input_frame, text="Add Task", command=self.add_task).grid(
            row=0, column=4, padx=5
        )

        # Task list
        self.tree = ttk.Treeview(
            main_frame, columns=("Task", "Priority", "Date", "Status"), show="headings"
        )
        self.tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure columns
        self.tree.heading("Task", text="Task")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Date", text="Date Added")
        self.tree.heading("Status", text="Status")

        self.tree.column("Task", width=250)
        self.tree.column("Priority", width=70)
        self.tree.column("Date", width=100)
        self.tree.column("Status", width=70)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            main_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=10)

        ttk.Button(button_frame, text="Mark Complete", command=self.mark_complete).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(button_frame, text="Delete Task", command=self.delete_task).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            button_frame, text="Clear Completed", command=self.clear_completed
        ).pack(side=tk.LEFT, padx=5)

        # Load existing tasks
        self.refresh_task_list()

    def add_task(self):
        task = self.task_var.get().strip()
        if task:
            task_info = {
                "task": task,
                "priority": self.priority_var.get(),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "status": "Pending",
            }
            self.tasks.append(task_info)
            self.save_tasks()
            self.refresh_task_list()
            self.task_var.set("")
        else:
            messagebox.showwarning("Warning", "Please enter a task!")

    def mark_complete(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            self.tasks[index]["status"] = "Completed"
            self.save_tasks()
            self.refresh_task_list()

    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            if messagebox.askyesno(
                "Confirm", "Are you sure you want to delete this task?"
            ):
                index = self.tree.index(selected_item)
                del self.tasks[index]
                self.save_tasks()
                self.refresh_task_list()

    def clear_completed(self):
        if messagebox.askyesno("Confirm", "Clear all completed tasks?"):
            self.tasks = [task for task in self.tasks if task["status"] != "Completed"]
            self.save_tasks()
            self.refresh_task_list()

    def refresh_task_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for task in self.tasks:
            self.tree.insert(
                "",
                tk.END,
                values=(task["task"], task["priority"], task["date"], task["status"]),
            )

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

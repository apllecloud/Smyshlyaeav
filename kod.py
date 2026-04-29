import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.trainings = self.load_trainings()

        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5)
        self.type_entry = tk.Entry(self.root)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        self.add_button = tk.Button(self.root, text="Добавить тренировку", command=self.add_training)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Фильтры
        tk.Label(self.root, text="Фильтр по типу:").grid(row=4, column=0, padx=5, pady=5)
        self.filter_type = ttk.Combobox(self.root, state="readonly")
        self.filter_type.grid(row=4, column=1, padx=5, pady=5)
        self.filter_type.bind("<<ComboboxSelected>>", self.apply_filters)

        tk.Label(self.root, text="Фильтр по дате (ДД.ММ.ГГГГ):").grid(row=5, column=0, padx=5, pady=5)
        self.filter_date = tk.Entry(self.root)
        self.filter_date.grid(row=5, column=1, padx=5, pady=5)
        self.filter_date.bind("<KeyRelease>", self.apply_filters)

        # Таблица
        columns = ("Дата", "Тип", "Длительность")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=6, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def validate_input(self, date_str, duration_str):
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ДД.ММ.ГГГГ")
            return False

        try:
            duration = float(duration_str)
            if duration <= 0:
                messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть числом")
            return False

        return True

    def add_training(self):
        date = self.date_entry.get()
        training_type = self.type_entry.get()
        duration = self.duration_entry.get()

        if not self.validate_input(date, duration):
            return

        training = {
            "date": date,
            "type": training_type,
            "duration": float(duration)
        }

        self.trainings.append(training)
        self.save_trainings()
        self.update_table()
        self.clear_inputs()

    def clear_inputs(self):
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    def load_trainings(self):
        try:
            with open("trainings.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_trainings(self):
        with open("trainings.json", "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=4)

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        types = set(t["type"] for t in self.trainings)
        self.filter_type["values"] = ["Все"] + list(types)
        self.filter_type.set("Все")

        for training in self.trainings:
            self.tree.insert("", "end", values=(
                training["date"],
                training["type"],
                f"{training['duration']} мин"
            ))

    def apply_filters(self, event=None):
        filtered = self.trainings

        filter_type = self.filter_type.get()
        if filter_type != "Все":
            filtered = [t for t in filtered if t["type"] == filter_type]

        filter_date = self.filter_date.get()
        if filter_date:
            filtered = [t for t in filtered if filter_date in t["date"]]

        for item in self.tree.get_children():
            self.tree.delete(item)

        for training in filtered:
            self.tree.insert("", "end", values=(
                training["date"],
                training["type"],
                f"{training['duration']} мин"
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()

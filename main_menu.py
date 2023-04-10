import tkinter as tk
from tkinter import ttk
from tkinter import LabelFrame
import sqlite3
from custom_window import ScheduleWindow

def get_column_names(table_name):
    with sqlite3.connect("schedule_manager.db") as connection:
        cursor = connection.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns_info = cursor.fetchall()
        column_names = [column_info[1] for column_info in columns_info]
    return column_names

class MainMenuWindow:
    def __init__(self, window):
        self.window = window
        self.window.title("Main Menu")
        self.window.geometry("300x200")

        ttk.Button(self.window, text="Classroom", command=lambda: self.open_table_window("Classroom")).grid(row=0, column=0, pady=20, padx=20, sticky=tk.W + tk.E)
        ttk.Button(self.window, text="Course", command=lambda: self.open_table_window("Course")).grid(row=1, column=0, pady=20, padx=20, sticky=tk.W + tk.E)
        ttk.Button(self.window, text="Professor", command=lambda: self.open_table_window("Professor")).grid(row=2, column=0, pady=20, padx=20, sticky=tk.W + tk.E)

    def open_table_window(self, table_name):
        field_names = get_column_names(table_name)
        table_window = tk.Toplevel()
        table_app = ScheduleWindow(table_window, field_names, table_name)
        table_window.wait_visibility()  # Add this line
        table_app.get_rows()

if __name__ == "__main__":
    root = tk.Tk()
    main_menu_app = MainMenuWindow(root)
    root.mainloop()

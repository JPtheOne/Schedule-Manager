from tkinter import *
from tkinter import ttk
import sqlite3

class CustomWindow:
    def __init__(self, window, field_names,table_name):
        #Creation of the window
        self.window = window
        self.window.title("CRUD APP MENU")
        self.window.geometry("1000x700")
        self.field_names = field_names
        self.table_name = table_name

        # Create a frame container
        frame = LabelFrame(self.window, text="Insert an item")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Inputs creation
        self.entries = {}
        for index, field_name in enumerate(self.field_names):
            Label(frame, text=f"{field_name}: ").grid(row=index + 1, column=0)
            entry = Entry(frame)
            entry.grid(row=index + 1, column=1)
            self.entries[field_name] = entry

        # Button creation
        ttk.Button(frame, text='Save new item', command=self.get_classrooms).grid(row=len(self.field_names) + 1, columnspan=2, sticky=W + E)
        # Other buttons can be added similarly as needed

        # Control messages
        self.message = Label(text='', fg="red")
        self.message.grid(row=len(self.field_names) + 2, column=0, columnspan=2, sticky=W + E)

        # Table parameters
        columns = [f"c{i}" for i in range(len(self.field_names))]
        self.tree = ttk.Treeview(column=tuple(columns), show='headings', height=8)
        self.tree.grid(row=len(self.field_names) + 3, column=0, columnspan=2)

        for index, field_name in enumerate(self.field_names):
            self.tree.column(f"# {index + 1}", anchor=CENTER)
            self.tree.heading(f"# {index + 1}", text=field_name)

        # Add your implementation for get_items()
        # self.get_items()

    def run_query(self, query, parameters=()):
        with sqlite3.connect("schedule_manager.db") as connection:
            cursor = connection.cursor()
            q_result = cursor.execute(query, parameters)
            connection.commit()
            return q_result

    def validating_inputs(self):
        validation = all(len(self.entries[field].get()) != 0 for field in self.field_names)
        return validation

    def get_classrooms(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        query = "Select * from {self.table_name}"
        db_rows = self.run_query(query)

        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=row)

if __name__ == "__main__":

    def get_column_names(table_name):
        with sqlite3.connect("schedule_manager.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns_info = cursor.fetchall()
            column_names = [column_info[1] for column_info in columns_info]
        return column_names


    root = Tk()
    TABLE = "PROFESSOR"
    field_names = get_column_names(TABLE)
    app = CustomWindow(root, field_names,TABLE)
    root.mainloop()

from tkinter import * 
import tkinter as tk
from tkinter import ttk

import sqlite3
from basicCRUD_methods import *

class ScheduleWindow:
    #All the design of the GUI window takes place here. The GUI adapts to the database table that will be manipulated
    def __init__(self, parent, window, field_names,table_name):
        #Window properties
        self.window = window
        self.parent = parent
        self.window.title("CRUD APP MENU")
        self.window.geometry("1000x1050")
        self.field_names = field_names
        self.table_name = table_name


        # Frame container(s)
        frame = LabelFrame(self.window, text= f"Insert a {table_name}")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Inputs creation
        self.entries = {}
        for index, field_name in enumerate(self.field_names):
            Label(frame, text=f"{field_name}: ").grid(row=index + 1, column=0)
            entry = Entry(frame)
            entry.grid(row=index + 1, column=1)
            self.entries[field_name] = entry

        # Button creation
        ttk.Button(frame, text=f'Save new {table_name}', command= self.insert_row).grid(row=len(self.field_names) + 1, column = 0, sticky=W + E)
        ttk.Button(frame, text=f'Delete {table_name}', command= self.delete_row).grid(row=len(self.field_names) + 1, column = 1, sticky=W + E)
        ttk.Button(frame, text=f'Update {table_name}', command = self.update_row).grid(row=len(self.field_names) + 1, column=2, sticky=W + E)

        # Control messages
        self.message = Label(text='', fg="red")
        self.message.grid(row=len(self.field_names) + 2, column=0, columnspan=2, sticky=W + E)

        # Display table parameters
        columns = [f"c{i}" for i in range(len(self.field_names))]
        self.tree = ttk.Treeview(column=tuple(columns), show='headings', height=8)
        self.tree.grid(row=len(self.field_names) + 3, column=0, columnspan=2)
        for index, field_name in enumerate(self.field_names):
            self.tree.column(f"# {index + 1}", anchor=CENTER)
            self.tree.heading(f"# {index + 1}", text=field_name)
        
        #Display information on crated table
        self.get_rows()

ScheduleWindow.run_query = run_query
ScheduleWindow.validating_inputs = validating_inputs
ScheduleWindow.get_rows = get_rows
ScheduleWindow.insert_row = insert_row
ScheduleWindow.delete_row = delete_row
ScheduleWindow.update_row = update_row
ScheduleWindow.edit_row = edit_row   

class MenuWindow:
    def __init__(self, window):
        self.window = window
        self.window.title("Menu")
        self.window.geometry("300x300")

        self.create_menu_buttons()

    def create_menu_buttons(self):
        for idx, table in enumerate(get_tables()):
            table_button = ttk.Button(self.window, text=table,
                                      command=lambda t=table: self.open_table(t))
            table_button.grid(row=idx, column=0, padx=5, pady=5, sticky=W+E)

    def open_table(self, table_name):
        table_window = Toplevel(self.window)
        field_names = get_field_names(table_name)
        ScheduleWindow(table_window, table_window, field_names, table_name)


    
if __name__ == "__main__":

    def get_field_names(table_name):
        with sqlite3.connect("schedule_manager.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns_info = cursor.fetchall()
            column_names = [column_info[1] for column_info in columns_info]
        return column_names

    def get_tables():
        with sqlite3.connect("schedule_manager.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
        return [table[0] for table in tables]
 



#MAIN TO RUN THROUGH MENU (STILL BUGGING)
    root = Tk()
    app = MenuWindow(root)
    root.mainloop()


#MAIN TO RUN THROUGH EACH TABLE (works better)
    """
    root = Tk()
    TABLE = "Classroom"
    field_names = get_field_names(TABLE)
    app = ScheduleWindow(root, field_names,TABLE)
    root.mainloop()
    """
from tkinter import *
from tkinter import ttk
import sqlite3
from CRUD_methods import *

class ScheduleWindow:
    #All the design of the GUI window takes place here. The GUI adapts to the database table that will be manipulated
    def __init__(self, window, field_names,table_name):
        #Window properties
        self.window = window
        self.window.title("CRUD APP MENU")
        self.window.geometry("1000x700")
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

    
if __name__ == "__main__":

    def get_column_names(table_name):
        with sqlite3.connect("schedule_manager.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns_info = cursor.fetchall()
            column_names = [column_info[1] for column_info in columns_info]
        return column_names


    root = Tk()
    TABLE = "Classroom"
    field_names = get_column_names(TABLE)
    app = ScheduleWindow(root, field_names,TABLE)
    root.mainloop()

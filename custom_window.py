from tkinter import *
from tkinter import ttk
import sqlite3

class ScheduleWindow:
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
       
    #Basic declaration of query. Essential for every DB operation
    def run_query(self, query, parameters=()):
        with sqlite3.connect("schedule_manager.db") as connection:
            cursor = connection.cursor()
            q_result = cursor.execute(query, parameters)
            connection.commit()
            return q_result

    #Checking all the entries are filled
    def validating_inputs(self):
        validation = all(len(self.entries[field].get()) != 0 for field in self.field_names)
        return validation

    #updating the visual table (R in CRUD)
    def get_rows(self):
        #Clear the zone before displaying
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        query = f"Select * from {self.table_name}"
        db_rows = self.run_query(query)

        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=row)

    #Insert a new row to the actual table (C in CRUD)
    def insert_row(self):
        if self.validating_inputs():
            query = f'INSERT INTO {self.table_name} ({", ".join(self.field_names)}) VALUES ({", ".join("?" * len(self.field_names))})'
            parameters = tuple(entry.get() for entry in self.entries.values())
            self.run_query(query, parameters)
            self.message["text"] = f"{self.table_name[:-1]} added successfully to the database"

            # Clear the entries
            for entry in self.entries.values():
                entry.delete(0, END)
        else:
            self.message["text"] = "Some essential data might be missing, try again please"
        self.get_rows()
   
    #Delete the selected row in actual table (D in CRUD)
    def delete_row(self):
        self.message['text'] = ""
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as error:
            self.message['text'] = "Please select an element"
            return
        self.message['text'] = ""

        primary_key_value = self.tree.item(self.tree.selection())['values'][0]
        query = f"DELETE FROM {self.table_name} WHERE {self.field_names[0]} = ?"
        self.run_query(query, (primary_key_value,))
        self.message["text"] = f"{self.table_name[:-1]} {primary_key_value} was deleted successfully"
        self.get_rows()


    def update_row(self):
        self.message['text'] = ""
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as error:
            self.message['text'] = "Please select an element"
            return
        primary_key_value = self.tree.item(self.tree.selection())['values'][0]
        self.edit_window = Toplevel()
        self.edit_window.title = "Edit Value"

        # Column selection
        Label(self.edit_window, text='Choose column to edit:').grid(row=0, column=1)
        selected_column = StringVar()
        column_dropdown = ttk.Combobox(self.edit_window, textvariable=selected_column)
        column_dropdown["values"] = self.field_names[1:]
        column_dropdown.grid(row=0, column=2)
        column_dropdown.current(0)

        # Old value
        Label(self.edit_window, text='Old value:').grid(row=1, column=1)
        old_value = StringVar()
        old_value_label = Label(self.edit_window, textvariable=old_value)
        old_value_label.grid(row=1, column=2)

        # New value
        Label(self.edit_window, text='New value:').grid(row=2, column=1)
        new_value = Entry(self.edit_window)
        new_value.grid(row=2, column=2)

        Button(self.edit_window, text="Update", command=lambda: self.edit_row(primary_key_value, selected_column.get(), old_value.get(), new_value.get())).grid(row=3, column=1, sticky=W + E)

        def on_column_change(event):
            column = selected_column.get()
            old_value.set(self.tree.item(self.tree.selection())['values'][self.field_names.index(column) - 1])

        column_dropdown.bind("<<ComboboxSelected>>", on_column_change)

    def edit_row(self, primary_key_value, selected_column, old_value, new_value):
        query = f"UPDATE {self.table_name} SET {selected_column} = ? WHERE {self.field_names[0]} = ?"
        params = (new_value, primary_key_value)
        self.run_query(query, params)
        self.edit_window.destroy()
        self.message['text'] = "Row updated with success"
        self.get_rows()

    
if __name__ == "__main__":

    def get_column_names(table_name):
        with sqlite3.connect("schedule_manager.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns_info = cursor.fetchall()
            column_names = [column_info[1] for column_info in columns_info]
        return column_names


    root = Tk()
    TABLE = "Course"
    field_names = get_column_names(TABLE)
    app = ScheduleWindow(root, field_names,TABLE)
    root.mainloop()

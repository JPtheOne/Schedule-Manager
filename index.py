from tkinter import ttk
from tkinter import *

import sqlite3
#  EXAMPLE MADE ONLY FOR CLASSROOM TABLE FROM DATABASE
class App:
    def __init__(self,window): #METHOD TO CREATE THE MAIN WINDOW
        self.window = window
        self.window.title("CRUD APP MENU")
        self.window.geometry("1000x700")

        #Create a frame container
        frame = LabelFrame(self.window, text ="Insert a classroom")
        frame.grid(row = 0, column = 0, columnspan=3, pady = 20)


        #Inputs creation
      
        Label(frame, text = 'Classroom code: ').grid(row = 1, column = 0)
        self.idClassroom_entry = Entry(frame)
        self.idClassroom_entry.grid(row = 1, column = 1)

        Label(frame, text = 'type: ').grid(row = 2, column = 0)
        self.type_entry = Entry(frame)
        self.type_entry.grid(row = 2, column = 1)

        Label(frame, text = 'location: ').grid(row = 3, column = 0)
        self.location_entry = Entry(frame)
        self.location_entry.grid(row = 3, column = 1)

        Label(frame, text = 'capacity: ').grid(row = 4, column = 0)
        self.capacity_entry = Entry(frame)
        self.capacity_entry.grid(row = 4, column = 1)



        #Button creation
        ttk.Button(frame, text = 'Save new classroom', command = self.insert_classroom).grid(row=5, columnspan = 2, sticky = W + E)


        #Control messages
        self.message = Label(text = '', fg = "red")
        self.message.grid(row = 3, column = 0, columnspan=2, sticky=W+E)
        #Table creation (NOT SQL). Tree keyword for instancing a table
        

        self.tree = ttk.Treeview (column=("c1", "c2","c3","c4"), show= 'headings', height= 8)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        
        self.tree.column("#1", anchor=CENTER)
        self.tree.heading("#1", text = "idClassroom")

        self.tree.column("#2", anchor=CENTER)
        self.tree.heading("#2", text = "type")

        self.tree.column("#3", anchor=CENTER)
        self.tree.heading("#3", text = "location")

        self.tree.column("#4", anchor=CENTER)
        self.tree.heading("#4", text = "capacity")        

        self.get_classrooms()

    def run_query(self,query, parameters=()): #BRINNG DATA BY QUERYING
        with sqlite3.connect("schedule_manager.db") as connection:
            cursor = connection.cursor()
            q_result = cursor.execute(query, parameters)
            connection.commit()
            return q_result
        
    def get_classrooms(self):
        #Cleaning table from previous data
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #obtaning table from sqlite
        query = "Select * from CLASSROOM ORDER BY idClassroom DESC"
        db_rows = self.run_query(query)
        #filling table
        for row in db_rows:
            self.tree.insert('',0, text = row[1], values = (row[0],row[1], row[2], row[3]))


    def validating_inputs (self):
        validation = len(self.idClassroom_entry.get()) != 0 and len(self.type_entry.get()) != 0 and len(self.location_entry.get()) != 0 and len(self.capacity_entry.get()) != 0 
        return validation
    

    
    def insert_classroom(self):
        if self.validating_inputs():
            query = 'insert into CLASSROOM values (?,?,?,?)'
            parameters = (self.idClassroom_entry.get(), self.type_entry.get(), self.location_entry.get(), self.capacity_entry.get())
            self.run_query(query,parameters)
            self.message["text"] = "Clasrrom {} added succesfully to database".format(self.idClassroom_entry.get())
        else:
            print("Some data is missing")
        self.get_classrooms()





















# Main function to start all the components
if __name__ == '__main__':
    window = Tk()
    application = App(window)
    window.mainloop()



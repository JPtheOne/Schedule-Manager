#***************************************** Complex CRUD Methods ***********************************************

#File storing the complex CRUD methods 
from datetime import datetime, timedelta
from tkinter import messagebox

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#Calculate end hour variable because SQLite does not support this operation
def calculate_end_hour(start_hour, duration):
    start_hour_dt = datetime.strptime(start_hour, "%H:%M")
    duration_parts = duration.split(':')
    hours, minutes = int(duration_parts[0]), int(duration_parts[1])
    end_hour_dt = start_hour_dt + timedelta(hours=hours, minutes=minutes)
    end_hour = end_hour_dt.strftime("%H:%M")
    return end_hour

#Complex constraints are validated for SCHEDULE table
def validate_schedule_insertion(self):
    course_id = self.entries["Course"].get()
    professor_id = self.entries["Professor"].get()
    classroom_id = self.entries["Classroom"].get()
    days = self.entries["Days"].get()
    start_time = self.entries["Start_time"].get()
    end_time = calculate_end_hour(start_time, self.entries["Duration"].get())

    # Constraint 0 & 1: End time must be calculated and the time will be inserted in the str("HH:MM") format
    if not end_time:
        messagebox.showerror("Error", "End time could not be calculated. Please check the input values.")
        return False

    # Constraint 2: Check foreign keys
    query = "SELECT ID FROM Course WHERE ID = ?"
    result = self.run_query(query, (course_id,))
    if not result.fetchone():
        messagebox.showerror("Error", "Course ID not found in the Course table.")
        return False

    query = "SELECT ID FROM Professor WHERE ID = ?"
    result = self.run_query(query, (professor_id,))
    if not result.fetchone():
        messagebox.showerror("Error", "Professor ID not found in the Professor table.")
        return False

    query = "SELECT ID FROM Classroom WHERE ID = ?"
    result = self.run_query(query, (classroom_id,))
    if not result.fetchone():
        messagebox.showerror("Error", "Classroom ID not found in the Classroom table.")
        return False

    # Constraint 3: Check if there is already a row with the same Course and Professor
    query = """SELECT * FROM Schedule
                WHERE Course = ? AND Professor = ? AND Days = ? AND
                      ((Start_time BETWEEN ? AND ?) OR
                       (End_time BETWEEN ? AND ?) OR
                       (Start_time < ? AND End_time > ?))"""
    params = (course_id, professor_id, days, start_time, end_time, start_time, end_time, start_time, end_time)
    result = self.run_query(query, params)
    if result.fetchone():
        messagebox.showerror("Error", "Schedule conflict detected for the same Course and Professor. Please check the input values.")
        return False

    # Constraint 4: Check if there is already a row with the same Classroom and Professor
    query = """SELECT * FROM Schedule
                WHERE Classroom = ? AND Professor = ? AND Days = ? AND
                      ((Start_time BETWEEN ? AND ?) OR
                       (End_time BETWEEN ? AND ?) OR
                       (Start_time < ? AND End_time > ?))"""
    params = (classroom_id, professor_id, days, start_time, end_time, start_time, end_time, start_time, end_time)
    result = self.run_query(query, params)
    if result.fetchone():
        messagebox.showerror("Error", "Schedule conflict detected for the same Classroom and Professor. Please check the input values.")
        return False
    return True

def print_PDF(self,table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('schedule_manager.db')
    
    # Use pandas to read the table data
    df = pd.read_sql_query(f"SELECT * from {table_name}", conn)
    
    # Close the connection
    conn.close()
    
    # Create a PdfPages object
    pdf_pages = PdfPages(f'{table_name} table.pdf')
    
    # Create a new figure and set the figsize
    fig, ax =plt.subplots(figsize=(12,4))
    
    # Remove the box around the plot
    ax.axis('tight')
    
    # Remove the y axis
    ax.axis('off')
    
    # Create a table and add it to the plot
    table = plt.table(cellText=df.values,
                      colLabels=df.columns,
                      cellLoc = 'center', 
                      loc='center')

    # Scale the table to fit the plot
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    
    # Save the figure to the PdfPages object
    pdf_pages.savefig(fig, bbox_inches='tight')
    
    # Close the PdfPages object
    pdf_pages.close()
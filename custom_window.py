from tkinter import *
from tkinter import ttk


class CustomWindow:
    def __init__(self, window, field_names):
        self.window = window
        self.window.title("CRUD APP MEN2222222U")
        self.window.geometry("1000x700")
        self.field_names = field_names

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
        ttk.Button(frame, text='Save new item', command=self.insert_item).grid(row=len(self.field_names) + 1, columnspan=2, sticky=W + E)
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

    def insert_item(self):
        pass  # Add your implementation for inserting an item

    # Add other functions as needed, such as delete_item(), update_item(), etc.


if __name__ == "__main__":
    root = Tk()
    field_names = ["product"]
    app = CustomWindow(root, field_names)
    root.mainloop()

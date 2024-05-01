import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
from scipy.optimize import linear_sum_assignment

def load_data():
    # ask the user to select a csv file
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not filepath:
        return
    
    # load data from csv, assuming the first column is unnamed and contains the topics
    data = pd.read_csv(filepath, sep=';', index_col=0)

    # convert all data to numeric, coercing errors will turn non-numeric to NaN
    data_numeric = data.apply(pd.to_numeric, errors='coerce')

    # determine the maximum existing priority and set missing values to this max + 1
    max_priority = data_numeric.max().max()
    data_filled = data_numeric.fillna(max_priority + 1)

    # solve the linear sum assignment problem
    cost_matrix = data_filled.values
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # prepare the results to be displayed in the treeview
    for i in tree.get_children():
        tree.delete(i)  # clear existing data in the table
    
    for row, col in zip(row_ind, col_ind):
        tree.insert("", 'end', values=(data_filled.index[row], data_filled.columns[col], data_filled.iloc[row, col]))

    # calculate the mean of the assigned priorities
    mean_priority = cost_matrix[row_ind, col_ind].mean()
    mean_label.config(text=f"Mean assigned priority: {mean_priority:.2f}")

# create the main window
root = tk.Tk()
root.title("Seminar Topic Allocation Tool")

# button frame for better alignment
button_frame = tk.Frame(root, padx=10, pady=10)
button_frame.pack(fill=tk.X, anchor='nw')

# add a button to load data
load_button = tk.Button(button_frame, text="Load CSV", command=load_data)
load_button.pack(side=tk.LEFT)

# create a treeview widget to display results in a table format
tree_frame = tk.Frame(root, padx=10)
tree_frame.pack(fill=tk.BOTH, expand=True)
tree = ttk.Treeview(tree_frame, columns=("Topic", "Student", "Priority"), show="headings")
tree.heading("Topic", text="Topic")
tree.heading("Student", text="Student")
tree.heading("Priority", text="Priority")
tree.column("Topic", anchor=tk.W, width=200)
tree.column("Student", anchor=tk.W, width=100)
tree.column("Priority", anchor=tk.CENTER, width=80)
tree.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

# create a label to display the mean priority, left-aligned
mean_label_frame = tk.Frame(root, padx=10, pady=10)
mean_label_frame.pack(fill=tk.X, anchor='w')
mean_label = tk.Label(mean_label_frame, text="", anchor="w")
mean_label.pack(side=tk.LEFT)

# start the GUI event loop
root.mainloop()